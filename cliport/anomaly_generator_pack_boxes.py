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
    __, reward,__,__ = env.step(act)
    output_queue.put((1,reward))
    event.set()

def one_episode_execution(info,obs,agent,env,task,add_anomaly=False,recording_step=0):
    #print("The step " + str(recording_step) + " execution will be recorded.")
    progress_list=task.inside_box_blocks.copy()
    for step in range(task.max_steps):
        act = agent.act(obs, info)
        if act==None:
            return None
        obj_id = act['obj_id']
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
                    anomaly_list=["pick","place","container","miss"]
                    # if len(progress_list)>0:
                    #     anomaly_list.append("progress")
                    type=random.choice(anomaly_list)
                    anomaly_generation = threading.Thread(target=anomaly_generator_for_primitive,
                                                          args=(env, output_queue, task, type,progress_list))
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
                __,anomaly = results[1]
            else:
                __, reward= results
                anomaly="No anomaly happened."

            rgb, depth = env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)


            info['answer'] += anomaly
            if reward>0 or type=="progress":
                print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')
                #episode.append((obs, None, reward, info)) ## only need to save the obs and text info
                return rgb_list,depth_list,info
            else:
                return None

        else:
            obs, reward, done, __ = env.step(act)
            print(f'| Goal: {info["lang_goal"]} | Question: {info["question"]} | Answer: {info["answer"]}')
            if reward>0:
                progress_list.append(obj_id)



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
    data_path = os.path.join(cfg['data_dir'],"{}-{}".format(cfg['task'], task.mode))
    dataset = RavensDataset(data_path, cfg, n_demos=0, augment=False)
    print(f"Saving to: {data_path}")
    print(f"Mode: {task.mode}")

    # Train seeds are even and val/test seeds are odd. Test seeds are offset by 10000
    seed = dataset.max_seed
    if seed < 0:
        if task.mode == 'train':
            seed = -2
        elif task.mode == 'val': # NOTE: beware of increasing val set to >100
            seed = -1
        elif task.mode == 'test':
            seed = -1 + 10000
        else:
            raise Exception("Invalid mode. Valid options: train, val, test")


    while dataset.n_episodes < cfg['n']:
        seed += 2

        # Set seeds.
        np.random.seed(seed)
        random.seed(seed)

        print('Oracle demo: {}/{} | Seed: {}'.format(dataset.n_episodes + 1, cfg['n'], seed))

        env.set_task(task)
        obs = env.reset()
        if obs is not None:
            info=env.info
            result = one_episode_execution(info, obs, agent, env, task, add_anomaly=True)
            if result != None:
                rgb_list, depth_list, info = result
                dataset.save_vlm_episodes(seed, rgb_list, depth_list, info, path=data_path)


if __name__ == '__main__':
    main()
