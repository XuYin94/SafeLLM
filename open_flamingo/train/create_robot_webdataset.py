import os
import argparse
import numpy as np
import tqdm
import uuid
import webdataset
import base64
from io import BytesIO
import os 
import re
from PIL import Image
import base64
import json
import pickle

pattern = r"'(.*?)'"
# Setup parameters for shard writers.
shard_writer_params = {
    "maxsize": 1024 * 1024 * 1024,  # 50 MB
    "maxcount": 1000,
    "keep_meta": True,
    "encoder": True,
}    
path_list=[
    'pack-box-primitive-train',
    'put-block-in-matching-bowl-train',
    'stack-block-pyramid-seq-unseen-colors-train'
]

def get_shard_pattern(path: str):
    base_pattern: str = "shard-%06d.tar"
    return os.path.join(path, base_pattern)



def load_field(root_path,field, fname):
    # Load sample from files.
    path = os.path.join(root_path,field)
    data = pickle.load(open(os.path.join(path, fname), 'rb'))
    #print(data)
    return data

def convert_pkl2shards_two_view(root_path,output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)    
    with webdataset.ShardWriter(get_shard_pattern(output_path), **shard_writer_params) as writer:
        
        for idx, task in enumerate(path_list):
            task_path=os.path.join(root_path,task)
            for __, type in enumerate(os.listdir(task_path)):
                for task in os.listdir(os.path.join(task_path,type)):
                    sub_path=os.path.join(task_path,type)
                    for field in ["view_0","view_3"]:
                        for fname in sorted(os.listdir(os.path.join(sub_path,field))):
                            language_x=""
                            sample_data={}
                            base64_images = []
                            episode_path=sorted(os.listdir(os.path.join(sub_path,field,fname)))
                            episode_path=[episode_path[0],episode_path[-1]]  ## only use the 1st/last render images to infer the robot action and the anomaly scene
                            for img_idx, img in enumerate(episode_path):
                                
                                #image = Image.open(os.path.join(sub_path,'font_img',fname,img)).convert("RGB")
                                with open(os.path.join(sub_path,field,fname,img),'rb') as img_file:
                                    img_bytes = img_file.read()
                                    img_str = base64.b64encode(img_bytes).decode("utf-8")
                                    base64_images.append(img_str)
                                language_x+="<image>"
                            question_text=load_field(sub_path,"info",fname+'.pkl')["question"]
                            answer_text=load_field(sub_path,"info",fname+'.pkl')["answer"]
                            action=re.findall(pattern, question_text)[0]
                            if field=="view_3":
                                question_text="Did the robot successfully execute the action '"+str(action)+"'? "
                                if 'succee' in type:
                                    answer_text="succeed"
                                else:
                                    answer_text="failed"
                                language_x+=question_text
                            else:
                                question_text="Did any anomaly happen during the execution of the action '"+str(action)+"'? "
                                language_x+=question_text
                                answer_text=''.join(answer_text.split(' and ')[1:])
                            language_x+="Answer: "+answer_text
                            language_x+="<|endofchunk|><|endoftext|>"
                            sample_data["img"]=base64_images
                            sample_data["text"]=language_x
                            key_str = uuid.uuid4().hex
                            sample_data=json.dumps(sample_data)
                            writer.write({"__key__": key_str, "json":sample_data})

def convert_pkl2shards(root_path,output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with webdataset.ShardWriter(get_shard_pattern(output_path), **shard_writer_params) as writer:
        
        for idx, task in enumerate(path_list):
            task_path=os.path.join(root_path,task)
            for __, type in enumerate(os.listdir(task_path)):
                for task in os.listdir(os.path.join(task_path,type)):
                    sub_path=os.path.join(task_path,type)
                    for field in ["view_0","view_3"]:
                        for fname in sorted(os.listdir(os.path.join(sub_path,field))):
                            language_x=""
                            sample_data={}
                            base64_images = []
                            episode_path=sorted(os.listdir(os.path.join(sub_path,field,fname)))
                            episode_path=[episode_path[0],episode_path[-1]]  ## only use the 1st/last render images to infer the robot action and the anomaly scene
                            for img_idx, img in enumerate(episode_path):
                                
                                #image = Image.open(os.path.join(sub_path,'font_img',fname,img)).convert("RGB")
                                with open(os.path.join(sub_path,field,fname,img),'rb') as img_file:
                                    img_bytes = img_file.read()
                                    img_str = base64.b64encode(img_bytes).decode("utf-8")
                                    base64_images.append(img_str)
                                language_x+="<image>"
                            question_text=load_field(sub_path,"info",fname+'.pkl')["question"]
                            answer_text=load_field(sub_path,"info",fname+'.pkl')["answer"]
                        
                            language_x+=question_text
                            language_x+="Answer: "

                            language_x+=answer_text
                            language_x+="<|endofchunk|><|endoftext|>"
                            sample_data["img"]=base64_images
                            sample_data["text"]=language_x
                            #sample=json.dumps({"image":base64_images,"text":language_x})
                            # with open("sample.json", "w") as outfile: 
                            #     json.dump(sample.decode("utf-8"), outfile)
                            key_str = uuid.uuid4().hex
                            sample_data=json.dumps(sample_data)
                            writer.write({"__key__": key_str, "json":sample_data})


if __name__ == "__main__":

    #convert_pkl2shards("/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm/","/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm/shards/one_view")
    convert_pkl2shards_two_view("/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm/","/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm/shards/two_view/")
    # data = pickle.load(open("/mnt/lynx1/users/zhang/Workfolder/data/primitive/pick-and-place-primitive-train/info/000012-26.pkl", 'rb'))
    # print(data)
    #data=load_field()
    #print(data)