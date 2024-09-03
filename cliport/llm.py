import logging
import re
from time import sleep
from typing import Union, List, Dict, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from prompt import general_prompt,cot_prompt_without_anomaly,cot_prompt_anomaly_handling_pick_place

import os
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"]="1"  

OPEN_SOURCE_LLMs = {"Llama-2-7b": 
                    {"path":"/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3-8B/",
                     "type": "completion"}, 
                    "Llama-3-8B": 
                    {"path": "/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3-8B/",
                     "type": "completion"},
                    "Llama-3-8B-instruct":
                     {"path":"/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3-8B-Instruct/",
                     "type": "instruction"}}


def combine_prompt_with_visual_feedback(feedback,message_history,is_initial=False):
    if not is_initial:
        prompt=message_history+"\n"+"Scene: "+feedback+"\n"
    else:
        prompt=message_history+"\n"+"Initial_state: "+feedback+"\n"
    return prompt


def get_next_step_plan(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None,length=32): 
    
    tokenizer, model,streamer= llm_args["tokenizer"], llm_args["model"],llm_args["streamer"]

    if feedback is not None:
        prompt = combine_prompt_with_visual_feedback(
            feedback,
            history_message
        )
    inputs = tokenizer(history_message, return_tensors="pt").to(model.device)
        # del inputs["token_type_ids"]
    ori_len=len(history_message)
    output = model.generate(
        **inputs,
        pad_token_id = tokenizer.eos_token_id,
        use_cache=True,
        max_new_tokens=length
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)[ori_len:]
    response = text_parsing(decoded_output)
    header_type=response.split(":")[0]
    return header_type,response

def text_parsing (generated_output: str):
    before_gen=generated_output.split('\n')[0]

    return before_gen


def load_llm(llm_name: str):
    logging.info("-" * 10 + f"Loading the LLM {llm_name}" + "-" * 10)
    assert llm_name in OPEN_SOURCE_LLMs.keys()
    path=OPEN_SOURCE_LLMs[llm_name]['path']
    tokenizer = AutoTokenizer.from_pretrained(path,TOKENIZERS_PARALLELISM=True)
    model = AutoModelForCausalLM.from_pretrained(
        path,
        device_map="auto",
        torch_dtype=torch.float16,
        rope_scaling={"type": "dynamic", "factor": 2}  # allows handling of longer inputs
    )
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))
    return tokenizer, model, streamer


def get_legal_action_plan(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None):
    generation_list=[]
    while True:
        header_type,response=get_next_step_plan(history_message,False,llm_args,feedback)
        #print(header_type)
        if header_type not in ["Scene", "User"]:        
            generation_list.append(response)
            history_message+=response+"\n"
        if header_type=="Robot_action":
            break
    return '\n'.join(generation_list),response






if __name__ == '__main__':

    feedback="The action 'pick up the orange block and palce it into the brown box' is exeuted successfully. No anmaly happened."
    i=0
    prompt=cot_prompt_anomaly_handling_pick_place+"\n"+"# put current-seen blocks in matching bowls.\nInitial_state: [white blowl, orange blowl, blue blowl, white block, orange block, blue block, red block, yellow block, pink block, brown block, green block, gray block, trash can]\n"
    print(prompt)
    tokenizer, model, streamer=load_llm("Llama-3-8B")
    llm_args = {
                "tokenizer": tokenizer,
                "model": model,
                "streamer": streamer
            }
    generation,action_plan=get_legal_action_plan(history_message=prompt,return_prompt = True,llm_args= llm_args,feedback=None)
    #print(action_plan)
    print(generation)