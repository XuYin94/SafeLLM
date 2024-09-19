"""Ravens main training script."""

import json
import logging
import os
import random
from PIL import Image
import hydra
from sklearn.metrics import confusion_matrix
import numpy as np
import torch
from matplotlib import pyplot as plt
from prompt_saycan import get_saycan_prompt,get_skill_set
from instructive_llm import llama_skill_generation_scoring
from cliport import agents
from cliport import dataset
from cliport import tasks
from cliport.environments.environment import Environment
from cliport.utils import utils
from cliport.utils.utils import anomaly_generator
import os
from llama3.llama import Llama
import threading, time,queue


def affordance_scoring(skill_set, task):
    affordance_list={}
    initial_state = task.initial_state
    pick_state, __, place_state = initial_state.partition("blocks")
    

    for skill in skill_set:
        inst=skill["name"]
        if inst=="done.":
            affordance_list[inst]=0.2
            continue
        pick, place = skill["pick"],skill["place"]
        affordance = 0
        
        if "Stacking" in task.task_name:
            if not 'stand' in place:
                place_info=pick_state
        else:
            place_info=place_state
        if pick in pick_state:
            if isinstance(place,list):
                if all(elem in place_info for elem in place):
                    affordance = 1
            else:
                if place in place_info:
                    affordance=1
        affordance_list[inst] = affordance
            
    return affordance_list

            

def normalize_scores(scores):
  max_score = max(scores.values())
  normed_scores = {key: np.clip(scores[key] / max_score, 0, 1) for key in scores}
  return normed_scores


def execution(obs,info,event,agent,env,output_queue):
    act=agent.act(obs,info)
    obs,reward, __, info=env.step(act)
    output_queue.put((1,obs,reward,info))
    event.set()
def one_step_execution(env,task,agent,obs,info,step,lang_inst,anomaly,handling_type="None",state=None):
    task.lang_goals=[lang_inst]
    info['lang_goal']=lang_inst
    print("Step {step}: {action}".format(step=step,action=lang_inst))
    if "done." in lang_inst or "alert." in lang_inst:
        env.add_video_frame()
        return 0.0
    
    event = threading.Event()
    output_queue = queue.Queue()
    actor = threading.Thread(target=execution,args=(obs,info,event,agent,env,output_queue))
    thread_list=[actor]
    
    if anomaly is not None:
        #env,output_queue,task=None,perturbation="pick",step=0,type="None",progress=None
        gt_anomaly=threading.Thread(target=anomaly_generator,args=(env,output_queue,task,anomaly,handling_type,state))
        thread_list.append(gt_anomaly)
    
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
        
    ## get the output of all threads 
    results=[]
    while not output_queue.empty():
        results.append(output_queue.get())
        
    if anomaly is not None:
        if len(results)<2:
            return None ## if the created perturbation fails
        results.sort()
        __, obs,reward,info = results[0]
        anomaly = results[1][1]
    else:
        __,obs,reward, info= results[0]
        anomaly="no anomaly happened."
    print(anomaly)
    return reward


        

@hydra.main(config_path='./cfg', config_name='eval_final')
def main(vcfg):
    # Load train cfg
    tcfg = utils.load_hydra_config(vcfg['train_config'])
    # Initialize environment and task.
    env = Environment(
        vcfg['assets_root'],
        disp=vcfg['disp'],
        shared_memory=vcfg['shared_memory'],
        hz=480,
        record_cfg=vcfg['record']
    )

    # Choose eval mode and task.
    mode = vcfg['mode']
    eval_task = vcfg['eval_task']
    if mode not in {'train', 'val', 'test'}:
        raise Exception("Invalid mode. Valid options: train, val, test")

    # Load eval dataset.
    dataset_type = vcfg['type']
    if 'multi' in dataset_type:
        ds = dataset.RavensMultiTaskDataset(
            vcfg['data_dir'],
            tcfg,
            group=eval_task,
            mode=mode,
            n_demos=vcfg['n_demos'],
            augment=False
        )
    else:
        ds = dataset.RavensDataset(
            os.path.join(vcfg['data_dir'], f"{eval_task}-{mode}"),
            tcfg,
            n_demos=vcfg['n_demos'],
            augment=False
        )

    name = '{}-{}-n{}'.format(eval_task, vcfg['agent'], vcfg['n_demos'])

    # Save path for results.
    json_name = f"multi-results-{mode}.json" if 'multi' in vcfg['model_path'] else f"results-{mode}-openflamingo.json"
    save_path = vcfg['save_path']
    print(f"Save path for results: {save_path}")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_json = os.path.join(save_path, f'{name}-{json_name}')

    # Load existing results.
    existing_results = {}
    if os.path.exists(save_json):
        with open(save_json, 'r') as f:
            existing_results = json.load(f)

    # Make a list of checkpoints to eval.
    ckpts_to_eval = list_ckpts_to_eval(vcfg, existing_results)
    
    generator = Llama.build(
    ckpt_dir="/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3.1-8B-Instruct/original",
    tokenizer_path="/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3.1-8B-Instruct/original/tokenizer.model",
    max_seq_len=1024,
    max_batch_size=64,
)

    task_name = vcfg['eval_task']
    anomaly_type=vcfg['anomaly_type'] ## choose the experiment type to determine the anomaly type 
    prompt, requirment=get_prompt(task_name,anomaly_type)
    record = vcfg['record']['save_video']
    n_demos = vcfg['n_demos']
    
    eval_results=[]
    for i in range(0, 100):
        logging.info(f'Test: {i + 1}/{n_demos}')
        episode, seed = ds.load(i)
        total_reward = 0
        total_nbr_action=0
        np.random.seed(seed)

        # set task

        task = tasks.names[task_name]()
        vlm_path=f"{vcfg['record']['vlm_path']}/episode_"+str(i)+""    
        if not os.path.exists(vlm_path):
            os.makedirs(vlm_path)
        task.mode = mode
        env.seed(seed)
        env.set_task(task)
        obs = env.reset()
        info = env.info

        initial_state = task.initial_state
        
        print("Initial State:", initial_state)
        handling_type=np.random.choice(["None"])
        if anomaly_type !='None':
            anomaly_time = 0#np.random.choice(np.arange(0, len(episode)-1), size=1, replace=False)  ## the step when the anomaly occurr
            print("{type} anomaly will occur in step {time}".format(type=anomaly_type,time=anomaly_time))
            if anomaly_type=="removal":
                if handling_type=="None":
                    alert_true.append(0)
                else:
                    alert_true.append(1)
        else:
            anomaly_time=-1
        episode_message=prompt+"### User:\n"+initial_state+"\n"
        ## implement SayCan plannning process
        all_llm_scores = []
        all_affordance_scores = []
        all_combined_scores = []
        options = get_skill_set(task=task_name)
        affordance_scores = affordance_scoring(options, task)
        #print(affordance_scores)
        num_tasks = 0
        steps_text = []
        while num_tasks<4:
            num_tasks += 1
            episode_message +="### User:\n"+"What is your plan for the next step?\n"+"### Assistant:\n"
            #llm_scores,__=llama_skill_scoring(episode_message, options, llm_args)
            llm_scores=llama_skill_generation_scoring(episode_message, options,generator)
            combined_scores = {option['name']: np.exp(llm_scores[option['name']]) * affordance_scores[option['name']] for option in options}
            combined_scores = normalize_scores(combined_scores)
            #print(combined_scores)
            selected_task = max(combined_scores, key=combined_scores.get)
            steps_text.append(selected_task+'.')
            print(num_tasks, "Selecting: ", selected_task)
            episode_message += selected_task + ".\n"
            #print(episode_message)
            all_llm_scores.append(llm_scores)
            all_affordance_scores.append(affordance_scores)
            all_combined_scores.append(combined_scores)
        #del generator
        torch.set_default_tensor_type(torch.cuda.FloatTensor)
        # Evaluation loop

        logging.info(f"Evaluating: {str(ckpts_to_eval)}")
        for ckpt in ckpts_to_eval:
            model_file = os.path.join(vcfg['model_path'], ckpt)

            if not os.path.exists(model_file) or not os.path.isfile(model_file):
                print(f"Checkpoint not found: {model_file}")
                continue
            elif not vcfg['update_results'] and ckpt in existing_results:
                print(f"Skipping because of existing results for {model_file}.")
                continue

            # Initialize agent.
            utils.set_seed(0, torch=True)
            agent = agents.names[vcfg['agent']](name, tcfg, None, ds,val=True)

            # Load checkpoint
            agent.load(model_file)
            #agent=agent.to(torch.bfloat16)
            logging.info(f"Loaded: {model_file}")

            # Run testing and save total rewards with last transition info.
            alert_true=[]
            alert_pred=[]
    
            #Start recording video (NOTE: super slow)
            if record:
                logging.info("Start recording video ......")
                video_name = f'{task_name}-{i + 1:06d}'
                if 'multi' in vcfg['model_task']:
                    video_name = f"{vcfg['model_task']}-{video_name}"
                env.start_rec(video_name)
                
            step=0
            state=0 
            occured=False
            for step, lang_inst in enumerate(steps_text):
                if lang_inst=="alert." and anomaly_type=="removal":
                    alert_pred.append(1)
                    if record:
                        env.end_rec()  
                        break
                
                if lang_inst=="done.":
                    env.end_rec()  
                    break
                
                
                if state ==anomaly_time and not occured:
                    anomaly= anomaly_type  
                    occured=True
                else:
                    anomaly=None
                results=one_step_execution(env,task,agent,obs,info,step,lang_inst,anomaly,handling_type,state=state)
                if results is None: 
                    break
                reward=results
                if reward>0:
                    state+=1
                total_reward+=reward
                total_nbr_action+=1
                                                
                __, __, done, __=env.step()
                if done:
                    env.end_rec()  
                    break
                step+=1
            if record:
                env.end_rec()
            eval_results.append((total_reward,total_nbr_action))
            mean_reward = np.mean([r for r, i in eval_results])
            mean_action=np.mean([i for r, i in eval_results])
            print(f'Mean_reward: {mean_reward} | Mean_action: {mean_action}')
    print(f'Mean_reward: {mean_reward} | Mean_action: {mean_action}')
    #print(total_reward)
    # all_results[ckpt] = {
    #     'SR': total_reward,
    #     'nbr_action':total_nbr_action
    # }
    # if anomaly_type=="removal":
    #     tn, fp, fn, tp = confusion_matrix(alert_true, alert_pred).ravel()
    #     all_results[ckpt]['tp']=tp
    #     all_results[ckpt]['fp']=fp
             
            


def list_ckpts_to_eval(vcfg, existing_results):
    ckpts_to_eval = []

    # Just the last.ckpt
    if vcfg['checkpoint_type'] == 'last':
        last_ckpt = 'last.ckpt'
        ckpts_to_eval.append(last_ckpt)

    # Validation checkpoints that haven't been already evaluated.
    elif vcfg['checkpoint_type'] == 'val_missing':
        checkpoints = sorted([c for c in os.listdir(vcfg['model_path']) if "steps=" in c])
        ckpts_to_eval = [c for c in checkpoints if c not in existing_results]

    # Find the best checkpoint from validation and run eval on the test set.
    elif vcfg['checkpoint_type'] == 'test_best':
        result_jsons = [c for c in os.listdir(vcfg['results_path']) if "results-val" in c]
        if 'multi' in vcfg['model_task']:
            result_jsons = [r for r in result_jsons if "multi" in r]
        else:
            result_jsons = [r for r in result_jsons if "multi" not in r]

        if len(result_jsons) > 0:
            result_json = result_jsons[0]
            with open(os.path.join(vcfg['results_path'], result_json), 'r') as f:
                eval_res = json.load(f)
            best_checkpoint = 'last.ckpt'
            best_success = -1.0
            for ckpt, res in eval_res.items():
                if res['mean_reward'] > best_success:
                    best_checkpoint = ckpt
                    best_success = res['mean_reward']
            ckpt = best_checkpoint
            ckpts_to_eval.append(ckpt)
        else:
            print("No best val ckpt found. Using last.ckpt")
            ckpt = 'steps.ckpt'
            ckpts_to_eval.append(ckpt)

    # Load a specific checkpoint with a substring e.g: 'steps=10000'
    else:
        print(f"Looking for: {vcfg['checkpoint_type']}")
        checkpoints = [c for c in os.listdir(vcfg['model_path']) if vcfg['checkpoint_type'] in c]
        checkpoint = checkpoints[0] if len(checkpoints) > 0 else ""
        ckpt = checkpoint
        ckpts_to_eval.append(ckpt)

    return ckpts_to_eval


def get_prompt(task:str,anomaly_type:str):
    requirment,prompt, system_info=get_saycan_prompt(task=task,anomaly_type=anomaly_type)
    prompt="### System: "+system_info+"\n"+prompt
    return prompt, requirment

if __name__ == '__main__':
    main()
