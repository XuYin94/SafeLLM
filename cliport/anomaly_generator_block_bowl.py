"""Data collection script."""

import os
import hydra
import numpy as np
import random
from cliport import tasks
import time
from cliport.dataset import RavensDataset
from cliport.utils.utils import anomaly_generator
from cliport.environments.environment import Environment
import threading, queue

def recording(env,rgb_list,depth_list,event):
    while not event.is_set():
        time.sleep(0.0001)
        rgb, depth = env.multi_view_render()
        rgb_list.append(rgb)
        depth_list.append(depth) ## if you want to save the depth info

def one_step_execution(env,act,event,output_queue,action_error=False):
    obs, reward, done,__ = env.step(act,action_error=action_error)
    output_queue.put((1,reward))
    event.set()

def one_episode_execution(agent,env,task,add_anomaly=False,action_error=False,recording_step=1):
    print("The step " + str(recording_step) + " execution will be recorded.")
    obs, reward, __, info = env.step()
    processed_objs=[]
    for step in range(task.max_steps):

        act = agent.act(obs, info)
        if act==None:
            return None

        obj_id = act['obj_id']
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
            if action_error:
                execution = threading.Thread(target=one_step_execution,
                                             args=(env, act, event, output_queue,True))
            else:
                execution = threading.Thread(target=one_step_execution,
                                             args=(env, act, event, output_queue,False))
            record_rgb = threading.Thread(target=recording,
                                          args=(env, rgb_list, depth_list,event))
            thread_list.append(execution)
            thread_list.append(record_rgb)
            if add_anomaly:
                if act is not None:
                    perturbation_list=["addition","removal"]
                    if len(processed_objs)>0:
                        perturbation_list.append("displacement")
                    perturbation_type=random.choice(perturbation_list)
                    type=random.choice(["distractor","None"])
                    anomaly_generation = threading.Thread(target=anomaly_generator,
                                                          args=(env, output_queue, task, perturbation_type,step,type,processed_objs))
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
                anomaly="no anomaly happened."
            if action_error:
                info['answer']="The action failed, and "

            rgb, depth = env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)

            info['answer'] += anomaly
            print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')

            if action_error:
                return rgb_list,depth_list,info
            elif add_anomaly:
                if reward>0:
                    return rgb_list, depth_list, info
                elif perturbation_type=="displacement":
                    return rgb_list, depth_list, info
                else:
                    return None
            else:
                return rgb_list, depth_list, info

        else:
            print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')
            obs, reward, done, info = env.step(act)
            if reward>0:
                processed_objs.append((color,obj_id))
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
    add_action_error=cfg['add_action_error']
    add_anomaly=cfg['add_anomaly']
    # Initialize scripted oracle agent and dataset.
    agent = task.oracle(env)
    episode_data_path = os.path.join(cfg['episode_data_dir'],"{}-{}".format(cfg['task'], task.mode))
    dataset = RavensDataset(episode_data_path, cfg, n_demos=0, augment=False)
    anomaly_data_path=os.path.join(cfg['data_dir'],"{}-{}".format(cfg['task'], task.mode))
    if add_action_error:
        anmaly_data_path=os.path.join(anomaly_data_path,"failure")
    else:
        anmaly_data_path = os.path.join(anomaly_data_path, "success")
    if add_anomaly:
        anmaly_data_path+="_pertubation"
    print(f"Saving to: {anmaly_data_path}")
    print(f"Mode: {task.mode}")

    save_idx=0
    if os.path.exists(anmaly_data_path):
        frame_list=sorted(os.listdir(os.path.join(anmaly_data_path,'info')))
        save_idx=len(frame_list)
        fname=frame_list[-1]
        seed = int(fname[(fname.find('-') + 1):-4])
    else:            
        seed = -2
    while save_idx < cfg['n']:
        seed += 2

        # Set seeds.
        np.random.seed(seed)
        random.seed(seed)
        env.set_task(task)
        env.reset()
        for recording_step in range (0,task.gt_step):
            result=one_episode_execution(agent,env,task,add_anomaly=add_anomaly,action_error=add_action_error,recording_step=recording_step)
            if result is not None:
                rgb_list,depth_list,info=result
                dataset.save_vlm_episodes(seed, rgb_list,depth_list,info,path=anmaly_data_path,idx=save_idx)
                save_idx+=1
            env.reset()


if __name__ == '__main__':
    main()
