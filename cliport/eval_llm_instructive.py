"""Ravens main training script."""

import json
import logging
import os

import hydra
import numpy as np
import torch
from matplotlib import pyplot as plt
from prompt import get_cot_prompt
from cliport import agents
from cliport import dataset
from cliport import tasks
from cliport.environments.environment import Environment
from cliport.utils import utils
from instructive_llm import load_llm,get_legal_LLM_feedback
from vlm import load_vlm, get_vlm_feedback
from cliport.utils.utils import anomaly_generator
import os
import threading, time,queue

def execution(obs,info,event,agent,env,output_queue):
    act=agent.act(obs,info)
    obs,reward, __, info=env.step(act)
    output_queue.put((1,obs,reward,info))
    event.set()

def one_step_execution(env,task,agent,obs,info,episode_message,llm_args,use_vlm,step,anomaly,state=None,vlm_args=None):
    episode_message+="### User:\nWhat is your plan for the next step?\n"
    header,lang_inst=get_legal_LLM_feedback(history_message=episode_message,return_prompt = True,llm_args= llm_args,feedback=None)
    episode_message+=header+'\n'+lang_inst+'\n'
    #print(lang_inst)

    task.lang_goals=[lang_inst]
    info['lang_goal']=lang_inst
    img_obs=[]
    print("Step {step}: {action}".format(step=step,action=lang_inst))
    if "done." in lang_inst or "alert." in lang_inst:
        env.add_video_frame()
        return episode_message,lang_inst,0.0,obs,info,None, step
    rgb_list=[]
    depth_list=[]
    rgb,depth= env.multi_view_render()
    rgb_list.append(rgb)
    depth_list.append(depth)
    
    event = threading.Event()
    output_queue = queue.Queue()
    actor = threading.Thread(target=execution,args=(obs,info,event,agent,env,output_queue))
    recorder=threading.Thread(target=record_img_for_reporter,args=(env,rgb_list,depth_list,event))
    thread_list=[actor,recorder]
    

    
    if anomaly is not None:
        #env,output_queue,task=None,perturbation="pick",step=0,type="None",progress=None
        gt_anomaly=threading.Thread(target=anomaly_generator,args=(env,output_queue,task,anomaly,step,"None",state))
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
    rgb, depth = env.multi_view_render()
    rgb_list.append(rgb)
    depth_list.append(depth)
    
    if not use_vlm: ## use the gt feedback from Pybullet
        #if reward>0:
        feedback="### User:\nThe action succeed, and "+anomaly+'\n'
    else:
        feedback=get_vlm_feedback(img_obs,lang_inst,vlm_args,device)+'\n'
    #env.add_video_frame(scene=feedback)
    episode_message+=feedback
    anomaly_desc=anomaly
    print(anomaly_desc)
    if "no anomaly" in anomaly_desc: ## start the next iteration after summarizing the progress and the future steps
        episode_message+="### User: \nPlease describe the achieved progress and the remaining goals.\n"
        header,state_of_progree_future=get_legal_LLM_feedback(history_message=episode_message,return_prompt = True,llm_args= llm_args,feedback=None)
        episode_message+=header+'\n'+state_of_progree_future+'\n'

        return episode_message,lang_inst,reward,obs,info,img_obs, step
    else:## start to reason the anomaly ascene
        episode_message+="### User:\nAnalyze the effect of the anomaly ['{anomaly}'] on the task regarding progress and feasibility.\n".format(anomaly=anomaly_desc)
        #print(episode_message)
        header, reply=get_legal_LLM_feedback(history_message=episode_message,return_prompt = True,llm_args= llm_args,feedback=None)
        #print(reply)
        episode_message+=header+'\n'+reply
        episode_message+="\n"+"### User:\nAnalyze the effect of the anomaly on future actions.\n"
        header, reply=get_legal_LLM_feedback(history_message=episode_message,return_prompt = True,llm_args= llm_args,feedback=None)
        #print(reply)
        episode_message+=header+'\n'+reply
        episode_message+="\n"+"### User:\nHow to handle this anomaly?\n"
        header, reply=get_legal_LLM_feedback(history_message=episode_message,return_prompt = True,llm_args= llm_args,feedback=None)
        #print(reply)
        episode_message+=header+'\n'+reply+'\n'
        #print(episode_message)
        obs, __, __, info=env.step()
        return one_step_execution(env,task,agent,obs,info,episode_message,llm_args,use_vlm,step,anomaly=None,state=state,vlm_args=vlm_args) ## assume no anomaly occurs in the recovery steps, otherwise the recurrsion will never stop
    ## save images 

        
        

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

    
    # Load LLM
    tokenizer, llm_model, streamer= load_llm(vcfg["planner"]['name'])
    llm_args = {
        "tokenizer": tokenizer,
        "model": llm_model,
        "streamer": streamer
    }

    # VLM
    task_name = vcfg['eval_task']
    use_vlm = vcfg["use_vlm"]
    anomaly_type=vcfg['anomaly_type'] ## choose the experiment type to determine the anomaly type 
    prompt, requirment=get_prompt(task_name,anomaly_type)
    # #Load VLM
    if use_vlm:
        vlm_path=os.path.join(save_path,'vlm')
        if not os.path.exists(vlm_path):
            os.makedirs(vlm_path)
        vlm_model, vis_processors, tokenizer = load_vlm("OpenFlamingo-9B-vitl-mpt7b", device)
        vlm_args = {
            "tokenizer": tokenizer,
            "model": vlm_model,
            "vis_processors": vis_processors
        }
    txt_path=vcfg['record']['txt_path']
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)

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
        logging.info(f"Loaded: {model_file}")

        record = vcfg['record']['save_video']
        n_demos = vcfg['n_demos']

        # Run testing and save total rewards with last transition info.
        for i in range(0, 50):
            text_path=os.path.join(txt_path,"episode_"+str(i)+".txt")
            if os.path.exists(text_path):
                os.remove(text_path)
            logging.info(f'Test: {i + 1}/{n_demos}')
            episode, seed = ds.load(i)
            total_reward = 0
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

            final_goal = task.final_goal
            initial_state = task.initial_state
            
            print(f'THE FINAL GOAL: {final_goal}')
            print("Initial State:", initial_state)
            
            if anomaly_type !='None':
                anomaly_time = 1#np.random.choice(np.arange(0, len(episode)-1), size=1, replace=False)  ## the step when the anomaly occurr
                print("{type} anomaly will occur in step {time}".format(type=anomaly_type,time=anomaly_time))
            else:
                anomaly_time=-1
            episode_message="### User:\n"+initial_state+"\nWhat is the final goal state?\n"

            episode_message=prompt+episode_message
            #print(episode_message)
            header,goal_state=get_legal_LLM_feedback(episode_message,None,llm_args,None)
            print(goal_state)
            episode_message+=header+'\n'+goal_state+'\n'
            
            
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
            print(len(episode_message))
            while step <task.max_steps:
                if step ==anomaly_time and not occured:
                    anomaly= anomaly_type  
                    occured=True
                else:
                    anomaly=None
                #print(state)
                if use_vlm:
                    results=one_step_execution(env,task,agent,obs,info,episode_message,llm_args,use_vlm,step,anomaly,state,vlm_args,vlm_path)
                else:
                    results=one_step_execution(env,task,agent,obs,info,episode_message,llm_args,use_vlm,step,anomaly,state)
                if results is None: 
                    break
                episode_message,act_plan,reward,obs,info,img_list, step=results
                print(reward)
                if reward>0:
                    state+=1
                    total_reward+=reward
                
                # if img_list is not None:
                #     for j, img in enumerate(img_list):
                #         save_name = f"{vlm_path}/step_{str(step)}_{str(j)}.png"
                #         plt.imsave(save_name, img)
                #print(len(act_plan))
                if act_plan=="alert.":
                    if record:
                        env.end_rec()  
                        break
                    
                if act_plan=="done.":
                    history=episode_message[len(prompt):]
                    if "All goals are completed" in history:
                        if record:
                            env.end_rec()  
                        break
                                # End recording video
                step+=1
            if record:
                env.end_rec()            
            execution_history=episode_message[len(prompt):]
            
            with open(text_path, 'a') as f:
                # Append a string to the file
                f.write(execution_history)
            



def record_img_for_reporter(env,rgb_list,depth_list,event):
    while not event.is_set():
        time.sleep(0.5)
        rgb, depth = env.multi_view_render()
        rgb_list.append(rgb)
        depth_list.append(depth)



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
    requirment,prompt, system_info=get_cot_prompt(task=task,anomaly_type=anomaly_type)
    prompt="### System: "+system_info+"\n"+prompt
    return prompt, requirment

if __name__ == '__main__':
    main()
