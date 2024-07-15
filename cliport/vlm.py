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
"lang_encoder_path": "anas-awadalla/mpt-1b-redpajama-200b",
"tokenizer_path": "anas-awadalla/mpt-1b-redpajama-200b"
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
    #checkpoint_path = hf_hub_download("openflamingo/OpenFlamingo-3B-vitl-mpt1b", "checkpoint.pt")
    vlm.load_state_dict(torch.load('/mnt/lynx4/users/zhang/yinxu/Workfolder/exp/vlm_exp/openflamingo3B/checkpoint_0.pt'.format(name=vlm_name)), strict=False)

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
    answer = output.split("Answer:")[1].strip("<|endofchunk|>").strip()

    return answer


def get_vlm_feedback(
        vlm_args: Dict,
        obs:List,
        inst: str,
        device=None,
):
    text_question="Did the robot successfully execute the action '{inst}'?, and did any anomaly happen?".format(inst=inst)
    #\print(text_question)
    tokenizer, vlm, vis_processor = vlm_args["tokenizer"], vlm_args["model"], vlm_args["vis_processor"]
    visual_input=[ vis_processor(img)for img in obs]
    vision_x=torch.stack(visual_input, dim=0).unsqueeze(1).unsqueeze(0).to(device)  ## convert the format to batch_size x num_media x num_frames x channels x height x width.
    #print(vision_x.shape)

    text_input="<image><image>{question} Answer: ".format(question=text_question)
    lang_x = tokenizer([text_input],return_tensors="pt",).to(device)
    generated_text = vlm.generate(
    vision_x=vision_x,
    lang_x=lang_x["input_ids"],
    attention_mask=lang_x["attention_mask"],
    max_new_tokens=64,
    num_beams=3,
    pad_token_id=50277


)   
    generated_text=tokenizer.decode(generated_text[0])
    feedback=parse_openflamingo_generation(generated_text)

    return feedback


if __name__=="__main__":
    import os
    device = torch.device("cuda:0") if torch.cuda.is_available() else "cpu"
    vlm, vis_processors, tokenizer=load_vlm("OpenFlamingo-3B-vitl-mpt1b",device)
    img_list=[Image.open(os.path.join("./test/",img)).convert("RGB") for img in os.listdir('./test/')]
    vlm_args = {
        "tokenizer": tokenizer,
        "model": vlm,
        "vis_processor": vis_processors
    }
    inst="place the orange block into the brown box"
    feedback=get_vlm_feedback(vlm_args,img_list,inst,device)
    print(feedback)