import os
import argparse
import numpy as np
import tqdm
import uuid
import webdataset
import base64
from io import BytesIO
import os 
from PIL import Image
import base64
import json
import pickle

def get_shard_pattern(path: str):
    base_pattern: str = "shard-%06d.tar"
    return os.path.join(path, base_pattern)



def load_field(root_path,field, fname):
    # Load sample from files.
    path = os.path.join(root_path,field)
    data = pickle.load(open(os.path.join(path, fname), 'rb'))
    #print(data)
    return data

def convert_pkl2shards(root_path,output_path):
    # Setup parameters for shard writers.
    shard_writer_params = {
        "maxsize": 1024 * 1024 * 1024,  # 50 MB
        "maxcount": 1000,
        "keep_meta": True,
        "encoder": True,
    }
    path_list=[
        'vlm/anomaly/',
        'primitive/'
    ]

    with webdataset.ShardWriter(get_shard_pattern(output_path), **shard_writer_params) as writer:
        
        for idx, type in enumerate(path_list):
            for task in os.listdir(os.path.join(root_path,type)):
                sub_path=os.path.join(root_path,type,task)
                for fname in sorted(os.listdir(os.path.join(sub_path,'font_img'))):
                    language_x=""
                    sample_data={}
                    base64_images = []
                    episode_path=sorted(os.listdir(os.path.join(sub_path,'font_img',fname)))
                    episode_path=[episode_path[0],episode_path[-1]]  ## only use the 1st/last render images to infer the robot action and the anomaly scene
                    for img_idx, img in enumerate(episode_path):
                        
                        #image = Image.open(os.path.join(sub_path,'font_img',fname,img)).convert("RGB")
                        with open(os.path.join(sub_path,'font_img',fname,img),'rb') as img_file:
                            img_bytes = img_file.read()
                            img_str = base64.b64encode(img_bytes).decode("utf-8")
                            base64_images.append(img_str)
                        language_x+="<image>"
                    #base64_images=np.concatenate(base64_images,axis=0)
                    #print(base64_images)
                    #print(sub_path)
                    #print(load_field(sub_path,"info",fname+'.pkl')["question"])
                    question_text=load_field(sub_path,"info",fname+'.pkl')[0]["question"]
                    answer_text=load_field(sub_path,"info",fname+'.pkl')[0]["answer"]
                  
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

    #convert_pkl2shards("/mnt/lynx1/users/zhang/Workfolder/data/","/mnt/lynx1/users/zhang/Workfolder/data/vlm/shards/")
    data = pickle.load(open("/mnt/lynx1/users/zhang/Workfolder/data/primitive/pick-and-place-primitive-train/info/000012-26.pkl", 'rb'))
    print(data)
    #data=load_field()
    #print(data)