"""Data collection script."""

import os
import hydra
import numpy as np
import random
from cliport import tasks
import time
from cliport.dataset import RavensDataset
from cliport.utils.utils import anomaly_generator_for_primitive
from cliport.environments.environment import Environment
import threading, queue

def recording(env,rgb_list,depth_list,event):
    while not event.is_set():
        time.sleep(0.0001)
        rgb, depth = env.multi_view_render()
        rgb_list.append(rgb)
        depth_list.append(depth)


def one_step_execution(env,act,event,output_queue,action_error=False):
    __, reward,__,__ = env.step(act,action_error)
    output_queue.put((1,reward))
    event.set()

def one_episode_execution(info,obs,agent,env,task,add_anomaly=False,action_error=False,recording_step=0):
    #print("The step " + str(recording_step) + " execution will be recorded.")
    progress_list=task.inside_box_blocks.copy()
    for __ in range(task.max_steps):
        act = agent.act(obs, info)
        if act==None:
            return None
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
                                         args=(env, act, event, output_queue, False))
        record_rgb=threading.Thread(target=recording,
                                          args=(env, rgb_list, depth_list,event))
        thread_list.append(execution)
        thread_list.append(record_rgb)
        if add_anomaly:
            if act is not None:
                perturbation_list=["addition"]
                if len(progress_list)>0:
                    perturbation_list.append("displacement")
                perturbation_type=random.choice(perturbation_list)
                anomaly_generation = threading.Thread(target=anomaly_generator_for_primitive,
                                                      args=(env, output_queue, task, perturbation_type,progress_list))
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
            return rgb_list, depth_list, info

        if add_anomaly:
            if reward <= 0 and perturbation_type!= "displacement":
                return None

        return rgb_list, depth_list, info


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
    data_path = os.path.join(cfg['data_dir'],"{}-{}".format(cfg['task'], task.mode))
    dataset = RavensDataset(data_path, cfg, n_demos=0, augment=False)

    if add_action_error:
        anmaly_data_path=os.path.join(data_path,"failure")
    else:
        anmaly_data_path = os.path.join(data_path, "success")
    if add_anomaly:
        anmaly_data_path+="_pertubation"

    print(f"Saving to: {data_path}")
    print(f"Mode: {task.mode}")

    # Train seeds are even and val/test seeds are odd. Test seeds are offset by 10000
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
        obs = env.reset()
        if obs is not None:
            info=env.info
            result = one_episode_execution(info, obs, agent, env, task, add_anomaly=add_anomaly,action_error=add_action_error)
            if result != None:
                rgb_list, depth_list, info = result
                dataset.save_vlm_episodes(seed, rgb_list, depth_list, info, path=anmaly_data_path,idx=save_idx)
                save_idx+=1


if __name__ == '__main__':
    main()
