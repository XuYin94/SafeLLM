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
    episode_list=get_normal_execution(task=task)[:3]
    
    random.shuffle(episode_list)
    print(len(episode_list))
        
    episode_list='\n'.join(episode_list)
    episode_list+="\n"
    system_prompt = ("You are a helpful assistant capable of decomposing high-level human instructions into low-level executable actions. In addition, you should analyze scene feedback to identify any anomaly conditions and provide appropriate corrective actions. For each task, break down the instructions into detailed steps and suggest corrective actions to address the issues if any anomalies are detected based on the scene feedback.\n")
    system_prompt+=please_help
    return please_help, episode_list, system_prompt





def get_normal_execution(task):
    
    if "match" in task:
        example_1 = ("### User:\n"+
                    "In the initial state, there are green, red, purple, and yellow blocks; there are green, red, purple, cyan, and blue bowls; and a trash can.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    #"The final goal state is ['Green, red, and purple blocks are in their corresponding bowls'].\n"+          
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the purple block in the purple bowl.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n"
                    )
        
        example_2 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, and orange bowls; and a trash can.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n") 
        
        example_3 = ("### User:\n"+
                    "In the initial state, there are white, red, pink, and green blocks; there are white, red, pink, yellow, and cyan bowls; and a trash can.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n")
                    
        example_4 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, orange, red, and white bowls; and a trash can.\n"+ 
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_5 = ("### User:\n"+
                    "In the initial state, there are white, green, yellow, orange, blue, and pink blocks; there are white, green, yellow, orange, and purple bowls; and a trash can.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_6=(
            "### User:\n"+
            "In the initial state, there are white, blue, yellow, green, pink, and red blocks; there are white, blue, yellow, orange, cyan, and purple bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the white block in the white bowl.\n"+
            #"### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            #"### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )
        
        example_7=(
            "### User:\n"+ 
            "In the initial state, there are red, green, blue, cyan, pink, and orange blocks; there are red, green, blue, cyan, yellow, and purple blocks; and a trash can.\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            #"### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            #"### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            #"### Assistant:\n"+
            "put the cyan block in the cyan bowl.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )
        
        example_8=(
            "### User:\n"+
            "In the initial state, there are purple, yellow, green, blue, white, and red blocks; there are purple, yellow, green, blue, orange, and pink bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the purple block in the purple bowl.\n"+
            #"### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            #"### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            #"### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            #"### Assistant:\n"+
            "done.\n"
            
        )
        example_9=(
            "### User:\n"+ 
            "In the initial state, there are orange, red, green, blue, pink, and cyan blocks; there are orange, red, green, blue, purple, and yellow bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the orange block in the orange bowl.\n"+
            #"### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            #"### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            #"### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )
        
        example_10=(
            "### User:\n"+ 
            "In the initial state, there are yellow, green, red, blue, orange, and purple blocks; there are yellow, green, red, blue, pink, and cyan bowls; and a trash can.\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            #"### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            #"### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            #"### Assistant:\n"+
            "done.\n"
            
        )
        episode_list=[example_1,example_2,example_3,example_4,example_5,example_6,example_7,example_8,example_9,example_10]
    
    elif task=="packing-boxes":
        episode_1=(
            "### User:\n"+
            "In the initial state, there are red, blue, green, yellow, orange, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, blue, and green blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the red block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the green block in the brown box.\n"+
            #"### Assistant:\n"+
            "done.\n")
        
        episode_2=(
            "### User:\n"+
            "In the initial state, there are orange, pink, orange, cyan, orange, pink, green, and gray blocks; there is a brown box and a trash can. The instruction is 'Please put the orange, pink and cyan blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the cyan block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            #"### Assistant:\n"+
            "done.\n")
        
        episode_3=("### User:\n"+
            "In the initial state, there are blue, gray, blue, green, white, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all blue, gray and green blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the green block in the brown box.\n"+
            #"### Assistant:\n"+
            "done.\n")

        episode_4=("### User:\n"+
            "In the initial state, there are red, red, green, gray, green, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, green, and gray blocks in the brown box'.\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the red block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the green block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            #"### Assistant:\n"+
            "put the green block in the brown box.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )

        episode_list=[episode_1,episode_2,episode_3,episode_4]
    
    elif "pyramid" in task:
        episode_1=(
            "### User:\n"+
            "In the initial state, there are gray, gray, blue, blue, blue, pink, and green blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, blue, and pink blocks'\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the gray block on the middle brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the blue block on the gray and gray blocks.\n"+
            #"### Assistant:\n"+
            "put the blue block on the gray and blue blocks.\n"+
            #"### Assistant:\n"+
            "put the pink block on the blue and blue blocks.\n"+
            #"### Assistant:\n"+
            "done.\n")
		
        episode_2 = (
            "### User:\n" +
            "In the initial state, there are yellow, blue, blue, orange, orange, brown, pink, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the yellow, blue, orange, and brown blocks'\n"+
            "### Assistant:\n"+
            "put the yellow block on the lightest brown block of the stand.\n" +
            #"### Assistant:\n"+
            "put the blue block on the middle brown block of the stand.\n" +
            #"### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the orange block on the yellow and blue blocks.\n" +
            #"### Assistant:\n"+
            "put the orange block on the blue and blue blocks.\n" +
            #"### Assistant:\n"+
            "put the brown block on the orange and orange blocks.\n" +
            #"### Assistant:\n"+
            "done.\n")
        
        episode_3=(
            "### User:\n" +
            "In the initial state, there are orange, purple, purple, purple, brown, brown, and pink blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the orange, purple, and brown blocks'\n"+
            "### Assistant:\n"+
            "put the orange block on the lightest brown block of the stand.\n" +
            #"### Assistant:\n"+
            "put the purple block on the middle brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the purple block on the darkest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the purple block on the orange and purple blocks.\n" +
            #"### Assistant:\n"+
            "put the brown block on the purple and purple blocks.\n"+
            #"### Assistant:\n"+
            "put the brown block on the purple and brown blocks.\n"+
            #"### Assistant:\n"+
            "done.\n")
        
        episode_4=(
            "### User:\n" +
            "In the initial state, there are gray, pink, gray, pink, pink, blue, and purple blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, pink, and blue blocks'\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the pink block on the middle brown block of the stand.\n" +
            #"### Assistant:\n"+
            "put the gray block on the darkest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the pink block on the gray and pink blocks.\n"+
            #"### Assistant:\n"+
            "put the pink block on the pink and gray blocks.\n"+
            #"### Assistant:\n"+
            "put the blue block on the pink and pink blocks.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )

        episode_5=(
            "### User:\n" +
            "In the initial state, there are blue, yellow, blue, blue, white, white, and orange blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, and white blocks'\n"+ 
            "### Assistant:\n"+
            "put the blue block on the lightest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the yellow block on the middle brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            #"### Assistant:\n"+
            "put the blue block on the blue and yellow blocks.\n"+
            #"### Assistant:\n"+
            "put the white block on the yellow and blue blocks.\n"+
            #"### Assistant:\n"+
            "put the white block on the blue and white blocks.\n"+
            #"### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
    return episode_list 




def get_skill_set(task="match"):
    skill_set=get_primitive_set(task)
    
    return skill_set


def get_primitive_set(task="match"):
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
        for color1 in ALL_COLORS:
            for color2 in ALL_COLORS:
                place_target.append("the "+color1+" and "+color2+" blocks")
                place_info.append([color1,color2])
    for i, pick_obj in enumerate(pick_target):
        for j, place in enumerate(place_target):
            skill_set.append(
                {
                    "name":"put the "+pick_obj+" "+position+" "+place+"",
                    "pick":pick_info[i],
                    "place":place_info[j]
                    })
            #skill_set.append("put the "+pick_obj+" block "+position+" "+place+"")
    skill_set.append({"name": "done."})
    return skill_set
