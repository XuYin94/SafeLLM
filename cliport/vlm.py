import logging
from pathlib import Path
from typing import Union, List,Dict

import torch
from PIL import Image
from huggingface_hub import hf_hub_download
from open_flamingo import create_model_and_transforms
from torchvision import transforms

model_name={

"OpenFlamingo-3B-vitl-mpt1b":{
"lang_encoder_path": "facebook/opt-1.3b",
"tokenizer_path": "facebook/opt-30b"
},
"OpenFlamingo-3B-vitl-mpt1b-dolly":{
    "lang_encoder_path":"anas-awadalla/mpt-1b-redpajama-200b-dolly",
    "tokenizer_path":"anas-awadalla/mpt-1b-redpajama-200b-dolly"
},
"OpenFlamingo-4B-vitl-rpj3b":{
"lang_encoder_path": "togethercomputer/RedPajama-INCITE-Base-3B-v1",
"tokenizer_path": "togethercomputer/RedPajama-INCITE-Base-3B-v1"
},
"OpenFlamingo-4B-vitl-rpj3b-langinstruct":
{
"lang_encoder_path": "togethercomputer/RedPajama-INCITE-Instruct-3B-v1",
"tokenizer_path": "togethercomputer/RedPajama-INCITE-Instruct-3B-v1"
},
}



def load_vlm(vlm_name: str, device: Union[torch.device, str]):
    # loads InstructBLIP pre-trained model
    logging.info("-" * 10 + f"Loading the VLM {vlm_name}" + "-" * 10)
    assert vlm_name in model_name.keys()
    model_config=model_name[vlm_name]
    
    vlm,__, txt_processors = create_model_and_transforms(
        clip_vision_encoder_path="ViT-L-14",
        clip_vision_encoder_pretrained="openai",
        lang_encoder_path=model_config["lang_encoder_path"],
        tokenizer_path=model_config["tokenizer_path"],
        cross_attn_every_n_layers=1
    )
    vlm.to(device)
    #state_dict = torch.load(hf_hub_download("openflamingo/OpenFlamingo-3B-vitl-mpt1b", "checkpoint.pt"))
    state_dict=torch.load('/mnt/bear1/users/zhangkang/yinxu/Workfolder/exp/OpenFlamingo-3B-vitl-mpt1b-dolly/single/checkpoint_4.pt')['model_state_dict']
    state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    vlm.load_state_dict(state_dict,strict=False)

    vis_processors=transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])
    return vlm, vis_processors, txt_processors

def parse_openflamingo_generation(output: str):
    """Extract the answer from the output combining prompts and answers.

    output example:
    <image><image>Did the robot successfully execute the action 'place the red block into the brown box', and did any anomaly happen? Answer: The action is executed successfully<|endofchunk|>
    """
    print(output)
    #print(output.split("Answer:")[-1].strip().split('<|endofchunk|>')[0])
    answer = output.split("Answer:")[-1].strip().split('<|endofchunk|>')[0]
    #print(answer)
    return answer


def get_vlm_feedback(
        vlm_args: Dict,
        obs:List,
        inst: str,
        device=None,
        configuration="single"
):
    tokenizer, vlm, vis_processor = vlm_args["tokenizer"], vlm_args["model"], vlm_args["vis_processor"]
    if configuration=="single":
        text_question="Did the robot successfully execute the action '{inst}'?, and did any anomaly happen?".format(inst=inst)
        #print(type(obs[0]))
        visual_input=[vis_processor(img)for img in obs]
        vision_x=torch.stack(visual_input, dim=0).unsqueeze(1).unsqueeze(0).to(device)  ## convert the format to batch_size x num_media x num_frames x channels x height x width.

        text_input=""
        for i in range(vision_x.shape[1]):
            text_input+="<image>"
        text_input+="Question: {question} Answer: ".format(question=text_question)
        #print(text_input)
        lang_x = tokenizer([text_input],return_tensors="pt",).to(device)
        generated_text = vlm.generate(
        vision_x=vision_x,
        lang_x=lang_x["input_ids"],
        attention_mask=lang_x["attention_mask"],
        max_new_tokens=64,
        num_beams=3,
        pad_token_id=50277)   
        generated_text=tokenizer.decode(generated_text[0])
        feedback=parse_openflamingo_generation(generated_text)
    else:
        ##font_view,topdown_view=obs[0],obs[1]
        question_list=["Did the robot successfully execute the action '{inst}'?".format(inst=inst), "Did any anomaly happen when the robot executed the action '{inst}'?".format(inst=inst)]
        Answer="The action {action_result}, and {pertur_desc}"
        feedback_list=[]
        #obs=[[view[0],view[-1]]for view in obs]
        for i in range(2):
            obs[i][0].save('./'+str(i)+'.png')
            visual_input=[vis_processor(img)for img in obs[i]]
            vision_x=torch.stack(visual_input, dim=0).unsqueeze(1).unsqueeze(0).to(device)  ## convert the format to batch_size x num_media x num_frames x channels x height x width.

            text_input=""
            for j in range(vision_x.shape[1]):
                text_input+="<image>"
            text_input+="Question: {question} Answer: ".format(question=question_list[i])
            lang_x = tokenizer([text_input],return_tensors="pt",).to(device)
            generated_text = vlm.generate(
            vision_x=vision_x,
            lang_x=lang_x["input_ids"],
            attention_mask=lang_x["attention_mask"],
            max_new_tokens=64,
            num_beams=3,
            pad_token_id=50277)
            output=tokenizer.decode(generated_text[0])   
            #print(parse_openflamingo_generation(output))
            feedback_list.append(parse_openflamingo_generation(output))
        feedback=Answer.format(action_result=feedback_list[0],pertur_desc=feedback_list[1])
            
    return feedback


if __name__=="__main__":
    import os
    input_path="/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/vlm/put-block-in-matching-bowl-train/failure_pertubation/view_0/000000-0"
    device = torch.device("cuda:0") if torch.cuda.is_available() else "cpu"
    vlm, vis_processors, tokenizer=load_vlm("OpenFlamingo-3B-vitl-mpt1b-dolly",device)
    vlm_args = {
        "tokenizer": tokenizer,
        "model": vlm,
        "vis_processor": vis_processors
    }
    inst="put the blue block in the blue bowl"
    img_list=[Image.open(os.path.join(input_path,img)).convert("RGB") for img in os.listdir(input_path)]
    feedback=get_vlm_feedback(vlm_args,img_list,inst,device,configuration="single")
    print(feedback)
    # input_path="/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/vlm/put-block-in-matching-bowl-train/failure_pertubation/view_3/000000-0"
    # img_list_2=[Image.open(os.path.join(input_path,img)).convert("RGB") for img in os.listdir(input_path)]
    # feedback=get_vlm_feedback(vlm_args,[img_list,img_list_2],inst,device,configuration="multi")
    # print(feedback)