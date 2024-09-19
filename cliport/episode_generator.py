"""Data collection script."""

import os
import hydra
import numpy as np
import random
import time
from cliport import tasks
from cliport.dataset import RavensDataset
from cliport.environments.environment import Environment
import cv2
from cliport.utils.utils import anomaly_generator
import pickle

def dump(path,data, field,eposide_id,seed):
    field_path = os.path.join(path, field)
    if not os.path.exists(field_path):
        os.makedirs(field_path)
    fname = f'{eposide_id:06d}-{seed}'
    if "img" in field:
        root_path = field_path + "/" + fname
        os.makedirs(root_path)
        for i, img in enumerate(data):
            cv2.imwrite(os.path.join(root_path, str(i) + ".png"), img)

    else:
        file_name = fname + '.pkl'  # -{len(episode):06d}
        with open(os.path.join(field_path, file_name), 'wb') as f:
            pickle.dump(data, f)



def episode_execution(info,obs,agent,env,task,episode):
    total_reward=0
    reward=0
    for i in range(task.max_steps):
        print(f'| Goal: {info["lang_goal"]}')
        act = agent.act(obs, info)
        episode.append((obs, act, reward, info))
        obs, reward, done, info = env.step(act)
        total_reward+=reward
        if done:
            break
    episode.append((obs, None, reward, info))
    return total_reward,episode


def one_step_execution(agent,env,obs,info,task,type,output_queue,event):
    act=agent.act(obs,info)
    anomaly_info=anomaly_generator(env,task,type=type,ora_act=act)
    obs, reward, __, info=env.step(act)
    output_queue.put(reward)
    output_queue.put(anomaly_info)
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
    for name in ["stack-block-pyramid-seq-seen-colors"]:
        task = tasks.names[name]()
        task.mode = cfg['mode']
        record = cfg['record']['save_video']

        # Initialize scripted oracle agent and dataset.
        agent = task.oracle(env)
        data_path = os.path.join(cfg['data_dir'],"episodes", "{}-{}".format(name, task.mode))
        #print(data_path)
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
                seed = -1 + 100000
            else:
                raise Exception("Invalid mode. Valid options: train, val, test")
        # Collect long-horizon training data from oracle demonstrations.
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

                total_reward,episode=episode_execution(info,obs,agent,env,task,episode)
                #print(len(episode))
                if total_reward > 0.99 :
                    dataset.add(seed, episode)




if __name__ == '__main__':
    main()
