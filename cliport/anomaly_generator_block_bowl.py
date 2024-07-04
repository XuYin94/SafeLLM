"""Data collection script."""

import os
import hydra
import numpy as np
import random
import cv2
from cliport import tasks
import time
from cliport.dataset import RavensDataset
from cliport.utils.utils import add_anomaly_object,anomaly_generator_for_primitive
from cliport.environments.environment import Environment
import threading, queue

def recording(env,rgb_list,depth_list,event):
    while not event.is_set():
        time.sleep(0.025)
        rgb, depth = env.multi_view_render()
        rgb_list.append(rgb)
        depth_list.append(depth)

def one_step_execution(env,act,event,output_queue):
    obs, reward, done,__ = env.step(act)
    output_queue.put((1,reward))
    event.set()

def one_episode_execution(agent,env,task,add_anomaly=False,recording_step=1):
    print("The step " + str(recording_step) + " execution will be recorded.")
    obs, reward, __, info = env.step()
    for step in range(task.max_steps):

        act = agent.act(obs, info)
        if act==None:
            return None
        obj_id = act['obj_id']
        if "matching" in task.task_name:
            for i, block_info in enumerate(task.block_info):
                if block_info[0]==obj_id:
                    color=block_info[1]
                    break
            info["lang_goal"]=info["lang_goal"].format(pick_color=color,place_color=color)
            info["question"]=info["question"].format(pick_color=color,place_color=color)
            info['answer']=info['answer'].format(pick_color=color,place_color=color)

        if step==recording_step:
            thread_list=[]
            rgb_list=[]
            depth_list=[]
            rgb,depth= env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)

            event = threading.Event()
            output_queue = queue.Queue()
            execution = threading.Thread(target=one_step_execution,
                                         args=(env, act, event, output_queue))
            record_rgb = threading.Thread(target=recording,
                                          args=(env, rgb_list, depth_list,event))
            thread_list.append(execution)
            thread_list.append(record_rgb)
            if add_anomaly:
                if act is not None:
                    anomaly_list=["progress"]
                    #if step>0 and "block" in task.task_name:
                        #anomaly_list.append("progress")
                    type=random.choice(anomaly_list)
                    #print(type)
                    anomaly_generation = threading.Thread(target=anomaly_generator_for_primitive,
                                                          args=(env, output_queue, task, type,step))
                    thread_list.append(anomaly_generation)
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
            results=[]
            while not output_queue.empty():
                results.append(output_queue.get())


            if add_anomaly:
                if len(results)<2:
                    return None
                results.sort()
                __, reward = results[0]
                anomaly = results[1][1]
            else:
                __, reward= results[0]
                anomaly="No anomaly happened."

            rgb, depth = env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)

            info['answer'] += anomaly
            if reward>0 or type=="progress":
                print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')
                return rgb_list,depth_list,info
            else:
                return None

        else:
            print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')
            obs, reward, done, info = env.step(act)
            if done:
                break




@hydra.main(config_path='./cfg', config_name='anomaly_data')
def main(cfg):
    # Initialize environment and task.
    env = Environment(
        cfg['assets_root'],
        disp=cfg['disp'],
        shared_memory=cfg['shared_memory'],
        hz=480,
        record_cfg=cfg['record']
    )
    task = tasks.names[cfg['task']]()
    task.mode = cfg['mode']

    # Initialize scripted oracle agent and dataset.
    agent = task.oracle(env)
    episode_data_path = os.path.join(cfg['episode_data_dir'],"{}-{}".format(cfg['task'], task.mode))
    dataset = RavensDataset(episode_data_path, cfg, n_demos=50, augment=False)
    anmaly_data_path=os.path.join(cfg['data_dir'],"{}-{}".format(cfg['task'], task.mode))
    print(f"Saving to: {anmaly_data_path}")
    print(f"Mode: {task.mode}")


    for i  in range (0,dataset.n_episodes):
        print(f'Test: {i + 1}/{50}')
        episode, seed = dataset.load(i)

        np.random.seed(seed)
        env.seed(seed)
        env.set_task(task)

        env.reset()
        env.set_task(task)
        recording_step=random.randint(1,task.gt_step-1)
        result=one_episode_execution(agent,env,task,add_anomaly=True,recording_step=recording_step)
        if result!=None:
            rgb_list,depth_list,info=result
            dataset.save_vlm_episodes(seed, rgb_list,depth_list,info,path=anmaly_data_path)



if __name__ == '__main__':
    main()
