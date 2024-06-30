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
                    {"path":"/mnt/lynx1/users/zhang/LLM_models/Meta-Llama-3-8B/",
                     "type": "completion"}, 
                    "Llama-3-8B": 
                    {"path": "/mnt/lynx1/users/zhang/LLM_models/Meta-Llama-3-8B/",
                     "type": "completion"},
                    "Llama-3-8B-instruct":
                     {"path":"//mnt/lynx1/users/zhang/LLM_models/Meta-Llama-3-8B-Instruct/",
                     "type": "instruction"}}
def text_parsing (generated_output: str):
    before_gen=generated_output.split('\n')[:2]

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



def get_next_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None,length=256): 
    
    tokenizer, model,streamer= llm_args["tokenizer"], llm_args["model"],llm_args["streamer"]

    if feedback is not None:
        history_message = history_message+"\n"+"### User:\n"+feedback+"\n"
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
    header_type,response=response[0],response[1]
    response=response.split('###')[0].strip()
    return header_type,response

def get_legal_LLM_feedback(history_message: str,return_prompt: bool = False,llm_args: Dict = None,feedback: str=None):
    while True:
        header_type,response=get_next_LLM_feedback(history_message,False,llm_args,feedback)
        #print(response)
        if header_type=="### Assistant:":
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