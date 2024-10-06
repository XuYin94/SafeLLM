import random
from utils.utils import ALL_COLORS, rel_pos

def get_help_infomation(task):
    if "matching" in task:
        please_help = (
            "The instruction is 'put current-seen blocks in bowls with matching colors'.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]' and that each step matches the color of the block to the color of the bowl.")
            #    "Ensure each step matches the color of the block to the color of the bowl.\n"
            #    "Explicitly verify and state the matching pairs and check if your planned blocks and bowls are present before estimating the goal state to avoid missing or wrong pairs.")
    elif "box" in task:
        please_help = (
            "The instruction is 'put current-seen blocks in the brown box'.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]'.")
    else:
        please_help=(
            "The instruction is 'Put blocks together to form a three-row pyramid'. \n"+
            "For the planned action steps, ensure each action follows the format 'put the [object1] on the [object2]'.")
    return please_help


def get_saycan_prompt(task, anomaly_type="pick"):
    please_help=get_help_infomation(task)
    episode_list=get_normal_execution(task=task)[:2]
    
    random.shuffle(episode_list)
    print(len(episode_list))
        
    episode_list='\n'.join(episode_list)
    episode_list+="\n"
    system_prompt = ("You are a helpful assistant capable of decomposing high-level human instructions into low-level actions.\n")
    system_prompt+=please_help
    return please_help, episode_list, system_prompt

def get_normal_execution(task):
    
    if "match" in task:
        example_1 = ("### User:\n"+
                    "In the initial state, there are green, red, purple, and yellow blocks; "+
                    "there are green, red, purple, cyan, and blue bowls; and a trash can.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+         
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the purple block in the purple bowl.\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n"
                    )
        
        example_2 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, and orange bowls; and a trash can.\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n") 
        
        example_3 = ("### User:\n"+
                    "In the initial state, there are white, red, pink, and green blocks; there are white, red, pink, yellow, and cyan bowls; and a trash can.\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
                    
        example_4 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, orange, red, and white bowls; and a trash can.\n"+ 
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_5 = ("### User:\n"+
                    "In the initial state, there are white, green, yellow, orange, blue, and pink blocks; there are white, green, yellow, orange, and purple bowls; and a trash can.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_6=(
            "### User:\n"+
            "In the initial state, there are white, blue, yellow, green, pink, and red blocks; there are white, blue, yellow, orange, cyan, and purple bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the white block in the white bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_7=(
            "### User:\n"+ 
            "In the initial state, there are red, green, blue, cyan, pink, and orange blocks; there are red, green, blue, cyan, yellow, and purple blocks; and a trash can.\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the cyan block in the cyan bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_8=(
            "### User:\n"+
            "In the initial state, there are purple, yellow, green, blue, white, and red blocks; there are purple, yellow, green, blue, orange, and pink bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the purple block in the purple bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
            
        )
        example_9=(
            "### User:\n"+ 
            "In the initial state, there are orange, red, green, blue, pink, and cyan blocks; there are orange, red, green, blue, purple, and yellow bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the orange block in the orange bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_10=(
            "### User:\n"+ 
            "In the initial state, there are yellow, green, red, blue, orange, and purple blocks; there are yellow, green, red, blue, pink, and cyan bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
            
        )
        episode_list=[example_1,example_2,example_3,example_4,example_5,example_6,example_7,example_8,example_9,example_10]
    
    elif task=="packing-boxes":
        episode_1=(
            "### User:\n"+
            "In the initial state, there are red, blue, green, yellow, orange, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, blue, and green blocks in the brown box'.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_2=(
            "### User:\n"+
            "In the initial state, there are orange, pink, orange, cyan, orange, pink, green, and gray blocks; there is a brown box and a trash can. The instruction is 'Please put the orange, pink and cyan blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the cyan block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_3=("### User:\n"+
            "In the initial state, there are blue, gray, blue, green, white, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all blue, gray and green blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
             "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")

        episode_4=("### User:\n"+
            "In the initial state, there are red, red, green, gray, green, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, green, and gray blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )

        episode_list=[episode_1,episode_2,episode_3,episode_4]
    
    elif "pyramid" in task:
        episode_1=(
            "### User:\n"+
            "In the initial state, there are gray, red, blue, brown, white, pink, and green blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, red, blue, brown, white, and pink blocks'.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the gray and red blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the red and blue blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the brown and white blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
		
        episode_2 = (
            "### User:\n" +
            "In the initial state, there are yellow, blue, red, orange, green, brown, pink, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the yellow, blue, red, orange, green and brown blocks'.\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the yellow block on the lightest brown block of the stand.\n" +
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the blue block on the middle brown block of the stand.\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the darkest brown block of the stand.\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the orange block on the yellow and blue blocks.\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block on the blue and red blocks.\n" +
            "### User:\n" +
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the brown block on the orange and green blocks.\n" +
	        "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "done.\n")
        
        episode_3=(
            "### User:\n" +
            "In the initial state, there are orange, purple, white, green, yellow, brown, and pink blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the orange, purple, white, green, yellow, and brown blocks'.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block on the lightest brown block of the stand.\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the purple block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the orange and purple blocks.\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the purple and white blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the purple and brown blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "done.\n")
        
        episode_4=(
            "### User:\n" +
            "In the initial state, there are gray, pink, yellow, red, green, blue, and purple blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, pink, yellow, red, green, and blue blocks'.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the middle brown block of the stand.\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the darkest brown block of the stand.\n"+
            "### User:\n" +
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the gray and pink blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the pink and yellow blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the blue block on the red and green blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )

        episode_5=(
            "### User:\n" +
            "In the initial state, there are blue, yellow, green, red, white, pink, and orange blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, white, and pink blocks'.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the yellow block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the blue and yellow blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the yellow and green blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the pink block on the red and white blocks.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
    return episode_list 




def get_skill_set(task="match",color_list=None):
    skill_set=get_primitive_set(task,color_list)
    
    return skill_set


def get_primitive_set(task="match",color_list=None):
    skill_set=[]
    pick_target=[color+' block' for color in ALL_COLORS]
    pick_info=[color for color in ALL_COLORS]
    if "match" in task:
        place_target=["the "+color+' bowl' for color in ALL_COLORS]
        place_info=[color for color in ALL_COLORS]
        position="in"
    elif "pack" in task:
        place_target=["brown box"]
        position="in"
        place_info=["brown box"]
    else:
        place_target=["the darkest brown block of the stand","the middle brown block of the stand","the lightest brown block of the stand"]

        position="on"
        place_info=['stand','stand','stand']
        for color1 in color_list:
            for color2 in color_list:
                place_target.append("the "+color1+" and "+color2+" blocks")
                place_info.append([color1,color2])
    for i, pick_obj in enumerate(pick_target):
        for j, place in enumerate(place_target):
            skill_name="put the "+pick_obj+" "+position+" "+place+""
            existing_list=[i['name'] for i in skill_set]
            if skill_name not in existing_list:
                skill_set.append(
                    {
                        "name":"put the "+pick_obj+" "+position+" "+place+"",
                        "pick":pick_info[i],
                        "place":place_info[j]
                        })
            #skill_set.append("put the "+pick_obj+" block "+position+" "+place+"")
    skill_set.append({"name": "done."})
    return skill_set
