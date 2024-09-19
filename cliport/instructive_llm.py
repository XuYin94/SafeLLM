import logging
import re
from time import sleep
from typing import Union, List, Dict, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from prompt import get_cot_prompt

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
                     "type": "instruction"},
                    "Llama-3.1-8B-instruct":
                     {"path":"/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3.1-8B-Instruct/",
                     "type": "instruction"}}
def text_parsing (generated_output: str):
    #print(generated_output)
    before_gen=generated_output.split('\n')[:2]
    #print(before_gen)
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

def get_next_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None,length=96): 
    
    tokenizer, model,streamer= llm_args["tokenizer"], llm_args["model"],llm_args["streamer"]
    inputs = tokenizer(history_message, return_tensors="pt").to(model.device)
        # del inputs["token_type_ids"]
    #print(history_message)
    ori_len=len(history_message)
    output = model.generate(
        **inputs,
        pad_token_id = tokenizer.eos_token_id,
        use_cache=True,
        max_new_tokens=length
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    #print(decoded_output)
    decoded_output=decoded_output[ori_len:]
    response = text_parsing(decoded_output)
    #print(response)
    header_type,response=response[0],response[1]
    response=response.split('###')[0].strip()
    return header_type,response

def get_legal_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None):
    while True:
        header_type,response=get_next_LLM_feedback(history_message,False,llm_args,feedback)
        #print(header_type)
        if "### Assistant:" == header_type:
            break
    return header_type,response



def llama_skill_generation_scoring(query, skill_set,generator,length=16,batch_size=8,option_start='\n'):
    scores={}
    prompt_list=[query+"### Assistant:\n"+skill['name']+'\n' for skill in skill_set]
    for i in range(0, len(prompt_list), batch_size):
        prompt_input= prompt_list[i:i + batch_size]
        skills=skill_set[i:i + batch_size]
        results = generator.text_completion(
                prompt_input,
                max_gen_len=length,
                temperature=0.6,
                top_p=0.9,
                logprobs=True
            )
        
        for skill, generation in zip(skills, results):
            inst=skill['name']
            #print(generation['generation'])
            token_logprobs = generation['logprobs']
            text_output=generation['tokens']
            # if inst=="done.":
            #     print(generation['generation'])
            
            total_logprob = 0
            assert len(text_output)==len(token_logprobs)
            for token, token_logprob in zip(reversed(text_output), reversed(token_logprobs)):

                if option_start==token:
                    #print("fuck")
                    break
                if token_logprob is not None:
                    total_logprob += token_logprob
            #print(inst)
            scores[inst] = total_logprob
    assert len(scores.keys())==len(skill_set)
    return scores


def get_next_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None,length=96): 
    
    tokenizer, model,streamer= llm_args["tokenizer"], llm_args["model"],llm_args["streamer"]
    inputs = tokenizer(history_message, return_tensors="pt").to(model.device)
        # del inputs["token_type_ids"]
    #print(history_message)
    ori_len=len(history_message)
    output = model.generate(
        **inputs,
        pad_token_id = tokenizer.eos_token_id,
        use_cache=True,
        max_new_tokens=length
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    #print(decoded_output)
    decoded_output=decoded_output[ori_len:]
    response = text_parsing(decoded_output)
    #print(response)
    header_type,response=response[0],response[1]
    response=response.split('###')[0].strip()
    return header_type,response

def get_legal_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None):
    while True:
        header_type,response=get_next_LLM_feedback(history_message,False,llm_args,feedback)
        #print(header_type)
        if "### Assistant:" == header_type:
            break
    return header_type,response



if __name__=="__main__":
    requirment,prompt, system_info=get_instructive_cot_pick_and_place()
    #white block, red block, green block, pink block, white bowl, red bowl, pink bowl, yellow bowl, cyan bowl, trash can
    new_episode=("### User: \n"
    f"{requirment}. In the initial state, there are blocks with white, orange, blue, red, yellow, pink colors, bowls with white, orange, blue, brown, green, gray colors, and a trash can. "
    "What is the final goal state?\n")
    
    #print(new_episode)
    text_input="### System: "+system_info+"\n"+prompt+new_episode
    
    #print(text_input)
    tokenizer, model, streamer=load_llm("Llama-3-8B-instruct")
    llm_args = {
                "tokenizer": tokenizer,
                "model": model,
                "streamer": streamer
            }
    generation,action_plan=get_legal_LLM_feedback(text_input,None,llm_args,None)
    print(action_plan)