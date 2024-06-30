"""Data collection script."""

import os
import hydra
import numpy as np
import random
import cv2
from cliport import tasks
import time
from cliport.dataset import RavensDataset
from cliport.utils.utils import add_anomaly_object
from cliport.environments.environment import Environment

def recording(env,rgb_list,depth_list,event):
    while not event.is_set():
        time.sleep(0.005)
        rgb, depth = env.multi_view_render()
        rgb_list.append(rgb)
        depth_list.append(depth)

def one_episode_execution(info,obs,agent,env,task,episode,output_queue,event,add_anomaly=False):
    for _ in range(task.max_steps):
        lang_goal = info['lang_goal']
        question = info['question']
        answer = info['answer']
        act = agent.act(obs, info)
        if add_anomaly:
            if 'trash can' in lang_goal:
                continue
            if act is not None:
                anomaly = add_anomaly_object(env, task, in_pick_position=True,oracle_pose=act)
        else:
            anomaly="no anomaly happened."
        obs, reward, __,__ = env.step(act)

        info['answer'] += anomaly
        answer+=anomaly
        print(info['lang_goal'])
        #print(reward)
        if reward>0: ## only need a single sucessful action
            reward=1.0
            print(
                f'| Goal: {lang_goal} | Question: {question} | Answer: {answer}')

            break
    episode.append((obs, act, reward, info))
    output_queue.put(reward)
    event.set()



@hydra.main(config_path='./cfg', config_name='data')
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
    record = cfg['record']['save_video']
    save_data = cfg['save_data']

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
        episode= []
        seed += 2

        # Set seeds.
        np.random.seed(seed)
        random.seed(seed)

        print('Oracle demo: {}/{} | Seed: {}'.format(dataset.n_episodes + 1, cfg['n'], seed))

        env.set_task(task)
        obs = env.reset()
        if obs is not None:

            info = env.info
            # Unlikely, but a safety check to prevent leaks.
            if task.mode == 'val' and seed > (-1 + 10000):
                raise Exception("!!! Seeds for val set will overlap with the test set !!!")

            # Start video recording (NOTE: super slow)
            if record:
                env.start_rec(f'{dataset.n_episodes+1:06d}')
            rgb_list=[]
            depth_list=[]
            rgb,depth= env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)

            import threading,queue
            event = threading.Event()
            output_queue = queue.Queue()
            execution=threading.Thread(target=one_episode_execution,args=(info,obs,agent,env,task,episode,output_queue,event))
            record_rgb=threading.Thread(target=recording,args=(env,rgb_list, depth_list,event))
            execution.start()
            record_rgb.start()
            execution.join()
            event.set()
            record_rgb.join()

            rgb,depth= env.multi_view_render()
            rgb_list.append(rgb)
            depth_list.append(depth)

            while not output_queue.empty():
                reward=output_queue.get()
            if save_data and reward > 0: ## for the primitive actions, only a single 
                dataset.add(seed, episode)
                dataset.save_vlm_episodes(seed,rgb_list,depth_list,path=data_path)




if __name__ == '__main__':
    main()
