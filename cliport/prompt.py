import random

def get_help_infomation(task):
    if "matching" in task:
        please_help = (
            "The task is 'Put blocks in bowls with matching colors'.\n" +
            "Before providing the action plan, please define the final goal state. Note that you should explicitly verify and state the matching pairs, ensuring your planned blocks and bowls have matching colors and are present in the initial state to avoid missing or incorrect pairs.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]' and that each step matches the color of the block to the color of the bowl.")
            #    "Ensure each step matches the color of the block to the color of the bowl.\n"
            #    "Explicitly verify and state the matching pairs and check if your planned blocks and bowls are present before estimating the goal state to avoid missing or wrong pairs.")
    elif "box" in task:
        please_help = (
            "The task is 'Pack blocks with specific colors in the brown box'.\n" +
            "Before providing the action plan, please define the state of the final goal. Please note that you only need to place the blocks with the target colors specified in the instructions.\n"+
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]'.")
    else:
        please_help=(
            "The task is 'Stack a Pyramid with current-seen blocks of specific Colors:'. \n"+
            "Before providing the action plan, please define the final goal state by specifying which blocks should be placed on the bottom, middle, and top rows.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] on the [object2]'.")
    return please_help


def get_cot_prompt(task, anomaly_type="pick"):
    please_help=get_help_infomation(task)
    #print(anomaly_type)
    if anomaly_type=="None":
        episode_list=get_normal_execution(task=task)[:3]
    elif anomaly_type!="combined":
        episode_list=get_normal_execution(task=task)
        episode_list+=[get_cot_handling_prompt(task=task,anomaly_type=anomaly_type)[1]]
    else:
        episode_list=[get_normal_execution(task=task)[0]]
        episode_list+=[get_cot_handling_prompt(task=task,anomaly_type="addition")[-1]]
        episode_list+=[get_cot_handling_prompt(task=task,anomaly_type="displacement")[0]]
    print(len(episode_list))
    #random.shuffle(episode_list)

        
    episode_list='\n'.join(episode_list)
    episode_list+="\n"
    system_prompt = ("You are a helpful assistant capable of decomposing high-level human instructions into low-level executable actions. In addition, you should analyze scene feedback to identify any anomaly conditions and provide appropriate corrective actions. For each task, break down the instructions into detailed steps and suggest corrective actions to address the issues if any anomalies are detected based on the scene feedback.\n")
    system_prompt+=please_help
    return please_help, episode_list, system_prompt



def get_normal_execution(task):
    
    if "-matching-bowl" in task:
        example_1 = ("### User:\n"+
                    "In the initial state, there are green, red, purple, and yellow blocks; there are green, red, purple, cyan, and blue bowls; and a trash can.\n"+
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
                    "The initial state includes the following matched block and bowl pairs: Green block -> Green bowl, Red block -> Red bowl, Purple block -> Purple bowl. Goal state: ['Green, red, and purple blocks in their matching bowls'].\n"+          
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n" +
                    "### User:\n"+
                    'The action succeeded, and no anomaly happened.\n'+
                    "### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "Progress: ['green block in green bowl']. Remaining goal: ['put the red and purple blocks in their matching bowls'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "The action failed, and no anomaly happened.\n"+
					"### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "Progress: ['green block in green bowl']. Remaining goal: ['put the red and purple blocks in their matching bowls'].\n" +
					"### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "Progress: ['green and red blocks in their matching bowls']. Remaining goal: ['put the purple block in its matching bowl'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the purple block in the purple bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['green, red and purple blocks in their matching bowls']. All goals are completed.\n" +
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "done.\n"
                    )
        
        example_2 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, and orange bowls; and a trash can.\n" +
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The initial state includes the following matched block and bowl pairs: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Orange block -> Orange bowl. Goal state: ['Yellow, blue, and orange blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action failed, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
					"### Assistant:\n"+
					"Progress: ['none of the blocks in their matching bowls']. Remaining goal: ['put the yellow, blue, orange, and orange blocks in their matching bowls'].\n"+
					"### User:\n"+
					"What is your next plan?\n"+
					"### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
					"### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "Progress: ['yellow block in yellow bowl']. Remaining goal: ['put the blue and orange blocks in their matching bowls'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['yellow and blue blocks in their matching bowls']. Remaining goal: ['put the orange block in its matching bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['yellow, blue, and orange blocks in their matching bowls.']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n") 
        
        example_3 = ("### User:\n"+
                    "In the initial state, there are white, red, pink, and green blocks; there are white, red, pink, yellow, and cyan bowls; and a trash can.\n" +
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The initial state includes the following matched block and bowl pairs: White block -> White bowl, Red block -> Red bowl, Pink block -> Pink bowl. Goal state:['White, red, and pink blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white block in white bowl']. Remaining goal: ['put the red and pink blocks in their matching bowls'].\n"+
                    "### User:\n"+"What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white and red blocks in their matching bowls']. Remaining goal: ['put the pink block in its matching bowl'.]\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "The action failed, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
					"### Assistant:\n"+
                    "Progress: ['white and red blocks in their matching bowls']. Remaining goal: ['put the pink block in its matching bowl'.]\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
					"### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white, red, and pink blocks in their matching bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan? \n"+
                    "### Assistant:\n"+
                    "done.\n")
                    

        example_4 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, orange, red, and white bowls; and a trash can.\n"+ 
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
                    "The initial state includes the following matched block and bowl pairs: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Orange block -> Orange bowl. Goal state: ['Yellow, blue, and orange blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['yellow block in yellow bowl']. Remaining goal: ['put the blue and orange blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['yellow and blue blocks in their matching bowls']. Remaining goal: ['put the orange block in its matching bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['yellow, blue, and orange blocks in their matching bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_5 = ("### User:\n"+
                    "In the initial state, there are white, green, yellow, orange, blue, and pink blocks; there are white, green, yellow, orange, and purple bowls; and a trash can.\n"+
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
					"The initial state includes the following matched block and bowl pairs: White block -> White bowl, Green block -> Green bowl, Yellow block -> Yellow bowl, Orange block -> Orange bowl. Goal state: ['White, green, yellow, and orange blocks in their matching bowls'].\n"+                   
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white block in white bowl']. Remaining goal: ['put the green, yellow, and orange blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white and green blocks in their matching bowls']. Remaining goal: ['put the yellow and orange blocks in their matching bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+"put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['the white, green, and yellow blocks are in their matching bowls']. Remaining goal: ['put the orange block in its matching bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe the progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "Progress: ['white, green, yellow, and orange blocks in their matching bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        episode_list=[example_1,example_2,example_3,example_4]
    
    elif task=="packing-boxes":
        episode_1=(
            "### User:\n"+
            "In the initial state, there are red, blue, red, green, blue, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, blue, and green blocks in the brown box'.\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Goal state: ['red block, blue block, red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block in the brown box']. Remaining goals: ['Put the blue block, red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
			"### Assistant:\n"+
            "Progress: ['red block in the brown box']. Remaining goals: ['Put the blue block, red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block and blue block in the brown box']. Remaining goals: ['Put the red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, blue block, and red block in the brown box']. Remaining goals: ['Put the green block and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, blue block, red block, and green block in the brown box']. Remaining goals: ['Put the blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, blue block, red block, and green block in the brown box']. Remaining goals: ['Put the blue block in the brown box'].\n"+
			"### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, blue block, red block, green block, and blue block in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_2=(
            "### User:\n"+
            "In the initial state, there are orange, pink, orange, cyan, orange, pink, green, and gray blocks; there is a brown box and a trash can. The instruction is 'Please put the orange, pink and cyan blocks in the brown box'.\n"+   
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Goal state: ['orange block, pink block, orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
			"### User:\n"+
            "The action failed, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['None of blocks in the brown box']. Remaining goals: ['Put the orange, pink block, orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block in the brown box']. Remaining goals: ['Put the pink block, orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block and pink block in the brown box']. Remaining goals: ['Put the orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block, pink block, and orange block in the brown box']. Remaining goals: ['Put the cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the cyan block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block, pink block, orange block, and cyan block in the brown box']. Remaining goals: ['Put the orange block and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block, pink block, orange block, and cyan block in the brown box']. Remaining goals: ['Put the orange block and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
			"### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block, pink block, orange block, cyan block, and orange block in the brown box']. Remaining goals: ['Put the pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block, pink block, orange block, cyan block, orange block, and pink block in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_3=("### User:\n"+
            "In the initial state, there are blue, gray, blue, green, white, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all blue, gray and green blocks in the brown box'.\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Goal state: ['blue block, gray block, blue block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block in the brown box']. Remaining goals: ['Put the gray block, blue block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block in the brown box']. Remaining goals: ['Put the gray block, blue block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
			"### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block and gray block in the brown box']. Remaining goals: ['Put the blue block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block and gray block in the brown box']. Remaining goals: ['Put the blue block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
			"### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block, gray block, and blue block in the brown box']. Remaining goals: ['Put the green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['blue block, gray block, blue block, and green block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")


        episode_4=("### User:\n"+
            "In the initial state, there are red, red, green, gray, green, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, green, and gray blocks in the brown box'.\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['red block, red block, green block, gray block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block in the brown box']. Remaining goals: ['Put the red block, green block, gray block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block and red block in the brown box']. Remaining goals: ['Put the green block, gray block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, red block, and green blocks in the brown box']. Remaining goals: ['Put the gray block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, red block, green block, and gray block in the brown box']. Remaining goals: ['Put the green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['red block, red block, green block, gray block, and green block in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4]
    
    elif "pyramid" in task:
        episode_1=(
            "### User:\n"+
            "In the initial state, there are gray, red, blue, brown, white, pink, and green blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, red, blue, brown, white, and pink blocks'\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Goal state:['gray, red, and blue blocks make the bottom row; brown and white blocks make the middle row; pink block makes the top row'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action failed, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
			"### Assistant:\n"+
            "Progress: ['None of the rows built']. Remaining goals: ['put the gray, red, and blue blocks on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
			"### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
			"### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### Assistant:\n"+
            "Progress: ['gray block on the stand']. Remaining goals: ['put the red and blue blocks on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['gray and red blocks on the stand']. Remaining goals: ['put the blue block on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
			"### User:\n"+
            "The action failed, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
			"### Assistant:\n"+
            "Progress: ['gray and red blocks on the stand']. Remaining goals: ['put the blue blocks on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
			"### User:\n"+
            "What is your next plan?\n"+
			"### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (gray, red, and blue blocks) is built']. Remaining goals: ['put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the gray and red blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (gray, red, and blue blocks) is built, the brown block is on top of the bottom row']. Remaining goals: ['put the white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the red and blue blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (gray, red, and blue blocks) and the middle row (brown and white blocks) are built']. Remaining goals: ['put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the brown and white blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (gray, red, and blue blocks), the middle row (brown and white blocks), and the top row (pink block) are built']. All goals are completed\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
		
        episode_2 = (
            "### User:\n" +
            "In the initial state, there are yellow, blue, red, orange, green, brown, pink, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the yellow, blue, red, orange, green and brown blocks'\n"+
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Goal state:['yellow, blue, and red blocks make the bottom row; orange and green blocks make the middle row; brown block makes the top row'].\n" +
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the yellow block on the lightest brown block of the stand.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['yellow block on the stand']. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the blue block on the middle brown block of the stand.\n" +
			"### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['yellow block on the stand']. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
			"### Assistant:\n" +
            "put the blue block on the middle brown block of the stand.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['yellow and blue blocks on the stand']. Remaining goals: ['put the red block on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the orange block on the yellow and blue blocks.\n" +
            "### User:\n" +
            "The action failed, and no anomaly happened.\n" +
			"### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the orange block on the yellow and blue blocks.\n" +
			"### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (yellow, blue, and red blocks) is built, orange block is on top of the bottom row']. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block on the blue and red blocks.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (yellow, blue, and red blocks) and middle row (orange and green blocks) are built']. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the brown block on the orange and green blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (yellow, blue, and red blocks), middle row (orange and green blocks), and top row (brown block) are built']. All goals are completed\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "done.\n")
        
        episode_3=(
            "### User:\n" +
            "In the initial state, there are orange, purple, white, green, yellow, brown, and pink blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the orange, purple, white, green, yellow, and brown blocks'\n"+
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Goal state:['orange, purple, and white blocks make the bottom row; green and yellow blocks make the middle row; brown block makes the top row'].\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block on the lightest brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange block on the stand']. Remaining goals: ['put the purple and white blocks on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the purple block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange and purple blocks on the stand']. Remaining goals: ['put the white block on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the darkest brown block of the stand.\n"+
			"### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['orange and purple blocks on the stand']. Remaining goals: ['put the white block on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (orange, purple, and white blocks) is built']. Remaining goals: ['put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the orange and purple blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom row (orange, purple, and white blocks) is built, and green block is on top of the bottom row']. Remaining goals: ['put the yellow block on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the purple and white blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (orange, purple, and white blocks) and middle row (green and yellow blocks) are built']. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the green and yellow blocks.\n"+
			"### User:\n"+
            "The action failed, and no anomaly happened.\n"+
			"### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (orange, purple, and white blocks) and middle row (green and yellow blocks) are built']. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the green and yellow blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (orange, purple, and white blocks), middle row (green and yellow blocks), and top row (brown block) are built']. All goals are completed\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "done.\n")
			
        episode_4=(
            "### User:\n" +
            "In the initial state, there are gray, pink, yellow, red, green, blue, and purple blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, pink, yellow, red, green, and blue blocks'\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Goal state: ['gray, pink, and yellow blocks make bottom row; red and green blocks make the middle row; blue block makes the top row'].\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['gray block on the stand']. Remaining goals: ['put the pink and yellow blocks on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the middle brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['gray and pink blocks on the stand']. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: ['bottom row (gray, pink, and yellow blocks) is built']. Remaining goals: ['put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n" +
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the gray and pink blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n" +
            "### Assistant:\n"+
            "Progress: ['bottom row (gray, pink, and yellow blocks) is built, and red block is on top of the bottom row']. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the pink and yellow blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['bottom (gray, pink, and yellow blocks) and middle row (red and green blocks) are built']. Remaining goals: ['put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the blue block on the red and green blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: ['bottom (gray, pink, and yellow blocks), middle row (red and green blocks), and top row (blue block) are built']. All goals are completed\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4]
    return episode_list 
    
    
def get_cot_handling_prompt(task, anomaly_type="pick"):
    if "-matching-bowl" in task:
        if anomaly_type=="removal":
            episode_1=(
                "### User:\n" +
                "In the initial state, there are gray, red, blue, brown, and white blocks; there are gray, red, blue, and yellow bowls; and a trash can.\n" +
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state contains the following pairs of blocks and matching bowls: Gray block -> Gray bowl, Red block -> Red bowl, Blue block -> Blue bowl. The brown and white blocks do not have corresponding bowls, and the yellow bowl does not have a corresponding block. The final goal state is ['Gray, red, and blue blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the gray block in the gray bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the white block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the white block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The gray block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the disappeared white block is not among the remaining target objects [red block, red bowl, blue block, blue bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block in the red bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the blue block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the blue block on the table disappeared] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The gray and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is affected since the disappeared blue block is among the remaining target objects [blue block, blue bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            episode_2=(
                "### User:\n" +
                "In the initial state, there are pink, cyan, yellow, blue, gray, and red blocks; there are pink, cyan, yellow, blue, green, and brown bowls; and a trash can.\n" +
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state contains the following pairs of blocks and matching bowls: Pink block -> Pink bowl, Cyan block -> Cyan bowl, Yellow block -> Yellow bowl, Blue block -> Blue bowl. The gray and red blocks do not have corresponding bowls, and the green and brown bowls do not have corresponding blocks. The final goal state is ['Pink, cyan, yellow, and blue blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the pink block in the pink bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the brown bowl on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the brown bowl on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The pink block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the disappeared brown bowl is not among the remaining target objects [cyan block, cyan bowl, yellow block, yellow bowl, blue block, blue bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the cyan block in the cyan bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the blue bowl on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the blue bowl on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The pink and cyan blocks are in their corresponding bowls'] is unaffected; the task feasibility is affected since the disappeared blue bowl is among the target object list [yellow block, yellow bowl, blue block, blue bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            
            episode_3=(
                "### User:\n" +
                "In the initial state, there are blue, green, red, yellow, white, and brown blocks; there are blue, green, red, yellow, and purple bowls; and a trash can.\n" +
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state contains the following pairs of blocks and matching bowls: Blue block -> Blue bowl, Green block -> Green bowl, Red block -> Red bowl, Yellow block -> Yellow bowl. The white and brown blocks do not have corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Blue, green, red, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the white block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the white block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The blue block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the disappeared white block is not among the remaining target objects [green block, green bowl, red block, red bowl, yellow block, yellow bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow bowl on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the yellow bowl on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The blue and green blocks are in their corresponding bowls'] is unaffected; the task feasibility is affected since the disappeared yellow bowl is among the target object list [red block, red bowl, yellow block, yellow bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            
            episode_4=(
                "### User:\n" +
                "In the initial state, there are blue, green, red, yellow, purple,  white, and brown blocks; there are blue, green, red, yellow, orange, and pink bowls; and a trash can.\n" +
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state contains the following pairs of blocks and matching bowls: Blue block -> Blue bowl, Green block -> Green bowl, Red block -> Red bowl, Yellow block -> Yellow bowl. The purple, white, and brown blocks do not have corresponding bowls, and the orange and pink bowls do not have their corresponding blocks. The final goal state is ['Blue, green, red, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the purple block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the purple block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The blue block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the disappeared purple block is not among the remaining target objects [green block, green bowl, red block, red bowl, yellow block, yellow bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the pink bowl on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the pink bowl on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The blue and green blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the disappeared pink bowl is not among the remaining target objects [red block, red bowl, yellow block, yellow bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your next plan?\n" +
                "### Assistant:\n"+
                "put the red block in the red bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe the progress and the remaining goals.\n'+
                "### Assistant:\n"+
                "The progress is ['the blue, green, and red blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowls'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe the progress and the remaining goals.\n'+
                "### Assistant:\n"+
                "The achieves progress is ['the blue, green, red and yellow blocks are in their corresponding bowls']. All goals are completed.\n" +
                "### User:\n"+
                "What is your next plan?\n" +
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_5=(
                "### User:\n" +
                "In the initial state, there are green, pink, yellow, blue, and red blocks; there are green, pink, yellow, and purple bowls; and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Pink block -> Pink bowl, Yellow block -> Yellow bowl. The blue and red blocks do not have corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Green, pink, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the yellow block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The green block is in its corresponding bowl'] is unaffected; the task feasibility is affected since the disappeared yellow block is among the target object list [pink block, pink bowl, yellow block, yellow bowl].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n" 
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
            
        elif anomaly_type=="displacement":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are cyan, yellow, orange, blue, red, and purple blocks; there are cyan, yellow, orange, blue, brown, and white bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Cyan block -> Cyan bowl, Yellow block -> Yellow bowl, Orange block -> Orange bowl, Blue block -> Blue bowl.  The red and purple blocks do not have corresponding bowls, and the brown and white bowls do not have their corresponding blocks. Goal state: ['Cyan, yellow, orange, and blue blocks are in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['none of the blocks in their matching bowls']. Remaining goal: ['put the cyan, yellow, orange, and blue blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block in cyan bowl']. Remaining goal: ['put the yellow, orange, and blue blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan and yellow blocks in their matching bowls']. Remaining goal: ['put the orange and blue blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the cyan and yellow blocks in their matching bowls are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the cyan and yellow blocks in their matching bowls are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the cyan and yellow blocks are not in their matching bowls; the current progress is ['the orange block is in its matching bowl']; the remaining target objects [cyan block, cyan bowl, yellow block, yellow bowl, blue block, blue bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the cyan and yellow blocks back to their matching bowls.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan and orange blocks in their matching bowls']. To address this anomaly, Remaining goal: ['put the yellow block in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['cyan, yellow, and orange blocks in their matching bowls']. Remaining goal: ['put the blue block in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action failed, and the cyan block in its matching bowl is moved to another position on the table.\n"+
				"### User:\n"+
                "Analyze the effect of the anomaly [the cyan block in its matching bowl is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the cyan block is not in its matching bowl; the current progress is ['yellow and orange block in their matching bowl']; the remaining target objects [cyan block, cyan bowl, blue block, blue bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the cyan block back to its matching bowls and attempt the blue block again.\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "Progress: ['cyan, yellow, and orange blocks in their matching bowls']. Remaining goal: ['put the blue block in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['cyan, yellow, orange, and blue blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_2 = (
                "### User:\n" +
                "In the initial state, there are green, purple, orange, blue, red, and yellow blocks; there are green, purple, orange, blue, brown, and black bowls; and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state includes the following matched block and bowl pairs: Green block -> Green bowl, Purple block -> Purple bowl, Orange block -> Orange bowl, Blue block -> Blue bowl. The red and yellow blocks do not have corresponding bowls, and the brown and black bowls do not have their corresponding blocks. Goal state: ['Green, purple, orange, and blue blocks are in their matching bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green block in green bowl']. Remaining goal: ['put the purple, orange, and blue blocks in their matching bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the purple block in the purple bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green and purple blocks in their matching bowls']. Remaining goal: ['put the orange and blue blocks in their matching bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the orange block in the orange bowl.\n" +
                "### User:\n" +
                "The action failed, and the green and purple blocks in their matching bowls are moved to other positions on the table.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the green and purple blocks in their matching bowls were moved to other positions on the table] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The Progress is disrupted, and the green and purple blocks are no longer in their matching bowls. The current progress is ['none of the blocks in their matching bowls ']; the remaining target objects [green block, green bowl, purple block, purple bowl, orange block, orange bowl, blue block, blue bowl] are available.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n"+
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Put the green and purple blocks back in their matching bowls and attempt the orange block again.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green block in its matching bowl']. Remaining goal: ['put the purple block in its matching bowl'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the purple block in the purple bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green and purple blocks in their matching bowls']. Remaining goal: ['put the orange block in its matching bowl'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the orange block in the orange bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The anomaly has been addressed. Progress: ['green, purple, and orange blocks in their matching bowls']. Remaining goal: ['put the blue block in its matching bowl'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green, purple, orange, and blue blocks in their matching bowls']. All goals are completed.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "done.\n"
            )


            
            anomaly_episode_list=[episode_1,episode_2]
        
        elif anomaly_type=="addition":
            ## add two episodes for "pick", "place", and "container", respectively.
            episode_1=(
                "### User:\n"+
                "In the initial state, there are blue, pink, red, purple, and white blocks; there are blue, pink, red, purple, yellow and cyan bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Blue block -> Blue bowl, Pink block -> Pink bowl, Red block -> Red bowl, Purple block -> Purple bowl. The white block does not have a corresponding bowl, and the yellow and cyan bowls do not have corresponding blocks. Goal state: ['Blue, pink, red, and purple blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['none of the blocks are in their matching bowls']. Remaining goal: ['put the blue, pink, red, and purple blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue block in blue bowl']. Remaining goal: ['put the pink, red, and purple blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['blue and pink blocks in their matching bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, purple block, purple bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [red block at the bottom right] for the target red block since they have the same color. \n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block at the bottom right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['blue and pink blocks in their matching bowls']. Remaining goal: ['put the red and purple block in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action failed, and a never-seen purple block appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple block appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['blue and pink blocks in their matching bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, purple block, purple bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [purple block at the top right] for the target purple block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion and attempt the red block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue and pink blocks in their matching bowls']. Remaining goal: ['put the red block in its matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['blue, pink, and red blocks in their matching bowls']. Remaining goal: ['put the purple block in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the purple bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue, pink, red, and purple blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")
            
            episode_2=(
                "### User:\n"+
                "In the initial state, there are green, yellow, red, blue, white, and cyan blocks; there are green, yellow, red, blue, and orange bowls; and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The initial state includes the following matched block and bowl pairs: Green block -> Green bowl, Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl.  The white and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. Goal state: ['Green, yellow, red, and blue blocks are in their matching bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and a never-seen white block appears at the bottom left.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [a never-seen white block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['green block in green bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, yellow bowl, red block, red bowl, blue block, blue bowl] are still available.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected since the anomaly block [white block at the bottom left] is not a target object and has a different color from any target blocks.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the yellow block in the yellow bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened." +
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['green and yellow blocks in their matching bowls']. Remaining goal: ['put the red and blue blocks in their matching bowls'].\n"+
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block in the red bowl.\n" +
                "### User:\n" +
                "The action failed, and a never-seen cyan block appears at the bottom left.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [a never-seen cyan block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['green and yellow in their matching bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, blue block, blue bowl] are still available.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected since the anomaly block [cyan block at the bottom left] is not a target object and has a different color from any target blocks.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block in the red bowl.\n" +
                "### User:\n" +
                "The action failed, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +						
                "### Assistant:\n"+
                "Progress: ['green and yellow blocks in their matching bowls']. Remaining goal: ['put the red and blue blocks in their matching bowls'].\n"+
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block in the red bowl.\n" +						
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +						
                "### Assistant:\n"+
                "Progress: ['green, yellow, and red blocks in their matching bowls']. Remaining goal: ['put the blue block in its matching bowls'].\n"+
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['green, yellow, red, and blue blocks in their matching bowls']. All goals are completed.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "done.\n")

            ## address the perturbation when the added block in the non-target bowls
            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, white, cyan, green, and yellow blocks; there are bowls with orange, white, cyan, and gray bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Orange block -> Orange bowl, White block -> White bowl, Cyan block -> Cyan bowl. The green and yellow blocks do not have corresponding bowls, and the gray bowl does not have a corresponding block. Goal state: ['Orange, cyan, and white blocks are in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block is placed into the white bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block is placed in the white bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['orange block in orange bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [white block, white bowl, cyan block, cyan bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [red block in the white bowl] takes the free space of the target white bowl, and the robot may not find a space to put the target white block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the white bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['orange block in orange bowl']. Remaining goal: ['put the white and cyan blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the white bowl.\n"+
                "### User:\n"+
                "The action failed, and a never-seen pink block is placed into the cyan bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block is placed in the cyan bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['orange block in orange bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [white block, white bowl, cyan block, cyan bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [pink block in the cyan bowl] takes the free space of the target cyan bowl, and the robot may not find a space to put the target cyan block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion and attempt the white block again.\n"+
		        "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the cyan bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['orange blocks in orange bowls']. Remaining goal: ['put the white block in its matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the white bowl.\n"+
                "### User:\n"+
                "The action succeed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"The anomaly has been addressed. Progress: ['orange and white blocks in their matching bowls']. Remaining goal: ['put the cyan block in its matching bowls'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['orange and white blocks in their matching bowls']. Remaining goal: ['put the cyan block in its matching bowls'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['orange, white, and cyan blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            
            episode_4=(
                "### User:\n"+
                "In the initial state, there are yellow, red, blue, green, and orange blocks; there are yellow, red, blue, purple, and cyan bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl. The green and orange blocks do not have corresponding bowls, and the purple and cyan bowls do not have corresponding blocks. Goal state: ['Yellow, red, and blue blocks are in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen cyan block is placed into the purple bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen cyan block is placed in the purple bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['yellow block in yellow bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [cyan block in the purple bowl] is not placed into any target bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action failed, and a never-seen green block appears in the cyan bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen green block appears in the cyan bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['yellow block in yellow bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [green block in the cyan bowl] is not placed into any target bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
				"### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['yellow block in yellow bowl']. Remaining goal: ['put the red and blue blocks in their matching bowls'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the red block in the red bowl.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['yellow and red blocks in their matching bowl']. Remaining goal: ['put the blue blocks in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow, red, and blue blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            ## address the perturbation when the addtion is the bowl
            episode_5=(
                "### User:\n"+
                "In the initial state, there are green, pink, gray, red, blue, and cyan blocks; there are green, pink, gray, and orange bowls; and a trash can.\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Green block -> Green bowl, Pink block -> Pink bowl, Gray block -> Gray bowl. The red, blue, and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. Goal state: ['Green, pink, and gray blocks are in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink bowl appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink bowl appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['green block in green bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, pink bowl, gray block, gray bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [pink bowl at the bottom right] for the target pink bowl since they have the same color. To avoid confusion, the anomaly bowl should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink bowl at the bottom right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['the green block is in its matching bowl']. Remaining goal: ['put the pink and gray blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action failed, and a never-seen gray bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['green block in green bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, pink bowl, gray block, gray bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [gray bowl at the bottom left] for the target gray bowl since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion and attempt the pink block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray bowl at the bottom left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['green block in green bowl']. Remaining goal: ['put the pink block in its matching bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['green and pink blocks in their matching bowls']. Remaining goal: ['put the gray block in its matching bowl'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['green and pink blocks in their matching bowls']. Remaining goal: ['put the gray block in its matching bowl'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['green, pink, and gray blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_6=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, pink, gray, and green blocks; there are yellow, blue, red, pink, and purple bowls; and a trash can.\n"+     
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state includes the following matched block and bowl pairs: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Red block -> Red bowl, Pink block -> Pink bowl. The gray and green blocks do not have their corresponding bowls, and the purple bowl does not have a corresponding block. Goal state: ['Yellow, blue, red, and pink blocks are in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block in yellow bowl']. Remaining goal: ['put the blue, red, and pink blocks in their matching bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen green bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen green bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['yellow and blue blocks in their matching bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, pink block, pink bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [green bowl at the bottom left] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
		        "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action failed, and a never-seen purple bowl appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple bowl appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['yellow and blue blocks in their matching bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, pink block, pink bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [purple bowl at the bottom right] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow and blue blocks in their matching bowls']. Remaining goal:['put the red and gray blocks in their matching bowls'].\n"+
				"### User:\n"+
				"What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
				"Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow, blue and red blocks in their matching bowls']. Remaining goal:['put the gray block in its matching bowl'].\n"+
				"### User:\n"+
				"What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow, blue, red, and pink blocks in their matching bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
        
        
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5,episode_6]
    elif "box" in task:
        if anomaly_type=="addition":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are red, red, green, yellow, orange, gray, and purple blocks; there is a brown box and a trash can. The instruction is 'please put all red, green, yellow, and orange blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['red block, red block, green block, yellow block, and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['red block in the brown box']. Remaining goals: ['Put the red block, green block, yellow block, and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears at the top left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears at the top left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['red block and red block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, orange block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [yellow block at the top left] for the target yellow block since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block at the top left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['red block and red block in the brown box']. Remaining goals: ['Put the green block, yellow block, orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['red block and red block in the brown box']. Remaining goals: ['Put the green block, yellow block, orange block in the brown box'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['red block, red block, and green block in the brown box']. Remaining goals: ['Put the yellow block and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and a never-seen orange block appears at the top right.\n"+
				"### User:\n"+
                "Analyze the effect of the anomaly [a never-seen orange block appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['red block, red block, and green block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, orange block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [orange block at the top right] for the target orange block since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion and attempt the yellow block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block at the top right into the trash can\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['red block, red block, and green block in the brown box']. To address this anomaly, the remaining goal is ['Put the yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"The anomaly has been addressed. Progress: ['red block, red block, green block, and yellow block in the brown box']. Remaining goals: ['Put the orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['red block, red block, green block, yellow block, and orange block in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")

            episode_2=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, cyan, pink, white, red, yellow, and orange blocks; there is a brown box and a trash can. The instruction is 'please put all cyan, pink, and white blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['cyan block, pink block, cyan block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['none of blocks in the brown box']. Remaining goals: ['Put the cyan block, pink block, cyan block, pink block, and white block in the brown box'].\n"+
				"### User:\n"+
				"What is your next plan?\n"+
				"### Assistant:\n"+
				"put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block in the brown box']. Remaining Goals: ['Put the pink block, cyan block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block and pink block in the brown box']. Remaining Goals: ['Put the cyan block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['cyan block, pink block, and cyan block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, white block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [yellow block appears at the top right] has a different color from any target blocks.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and a never-seen red block appears at the bottom right.\n"+
				"### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['cyan block, pink block, and cyan block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, white block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [red block appears at the bottom right] has a different color from any target blocks.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block, pink block, cyan block, and pink block in the brown box']. Remaining Goals: ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block, pink block, cyan block, pink block, and white block in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")
            
            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, purple, white, white, gray, pink, and green blocks; there is a brown box and a trash can. The instruction is 'please put all orange, purple, and white blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['orange block, purple block, white block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['orange block in the brown box']. Remaining Goals: ['Put the purple block, white block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears in the brown box.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears in the brown box] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['orange block and purple block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [white block, white block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [yellow block in the brown box] takes the free space of the brown box, and the robot may not find a space to put the target block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['orange block and purple block in the brown box']. Remaining Goals: ['Put the white and white blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and a never-seen pink block appears in the brown box.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears in the brown box] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['orange block and purple block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [white block, white block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [pink block in the brown box] takes the free space of the brown box, and the robot may not find a space to put the target block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion and attempt the white block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box into the trash can.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['orange block and purple block in the brown box']. Remaining Goals: ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['orange block, purple block, and white block in the brown box']. Remaining Goals: ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['orange block, purple block, white block, and white block in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_4=(
                "### User:\n"+
                "In the initial state, there are gray, blue, gray, cyan, cyan, orange, yellow, and red blocks; there is a brown box and a trash can. The instruction is 'Please put all gray, blue, and cyan blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['gray block, blue block, gray block, cyan block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['gray block in the brown box']. Remaining goals: ['Put the blue block, gray block, cyan block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and a never-seen brown box appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen brown box appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['gray block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, gray block, cyan block, cyan block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly box [brown box at the top right] as the target brown box since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly box to prevent confusion and attempt the blue block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the brown box at the top right into trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['gray block in the brown box']. Remaining goals: ['Put the blue block in the brown box'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['gray block and blue block in the brown box']. Remaining goals: ['Put the gray block, cyan block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen brown box appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen brown box appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['gray block, blue block, and gray block in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [cyan block, cyan block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly box [brown box at the bottom right] as the target brown box since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly brown box to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the brown box at the bottom right into trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['gray block, blue block, and gray block in the brown box']. Remaining goals: ['Put the cyan and cyan blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['gray block, blue block, gray block, and cyan block in the brown box']. Remaining goals: ['Put the cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
				"### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['gray block, blue block, gray block, and cyan block in the brown box']. Remaining goals: ['Put the cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['gray block, blue block, gray block, cyan block, and cyan block in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4]
    
        elif anomaly_type=="displacement":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are yellow, red, red, blue, yellow, purple, and gray blocks; there is a brown box and a trash can. The instruction is 'please put all yellow, red, and blue blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['yellow block, red block, red block, blue block, and yellow block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block in the brown box']. Remaining goals: ['Put the red block, red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block in the brown box']. Remaining goals: ['Put the red block, red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block and red block in the brown box']. Remaining goals: ['Put the red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the yellow and red blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the yellow and red blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the yellow and red blocks are not in the brown box; the current progress is ['red block in the brown box']. The task feasibility is unaffected since the remaining target objects [yellow block, red block, blue block, yellow block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the yellow and red blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block and red block in the brown box']. Remaining goals: ['Put the red block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['yellow block, red block, and red block in the brown box']. Remaining goals: ['Put the blue and yellow blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
				"### User:\n"+
                "The action failed, and the red block in the brown box is moved to another position on the table.\n"+
				"### User:\n"+
                "Analyze the effect of the anomaly [the red block in the brown box is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The rogress is disrupted, and the red block is not in the brown box; the current progress is ['yellow block, red block in the brown box']. The task feasibility is unaffected since the remaining target objects [red block, blue block, yellow block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the red block back in the brown box to resume progress and attempt the blue block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block, red block, and red block in the brown box']. Remaining goals: ['Put the blue block in the brown box'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['yellow block, red block, red block, and blue block are in the brown box']. Remaining goals: ['Put the yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block, red block, red block, blue block, and yellow block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
                )
            episode_2=(
                "### User:\n"+
                "In the initial state, there are pink, gray, gray, cyan, gray, red, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all pink, gray, and cyan blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['pink block, gray block, gray block, cyan block, and gray block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['pink block in the brown box']. Remaining goals: ['Put the gray block, gray block, cyan block, and gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and the pink block in the brown box is moved to another position on the table.\n"+
				"### User:\n"+
                "Analyze the effect of the anomaly [the pink block in the brown box is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the pink block is not in the brown box; the current progress is ['none of blocks in the brown box']. The task feasibility is unaffected since the remaining target objects [pink block, gray block, gray block, cyan block, and gray block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the pink block back in the brown box to resume progress and attempt the gray block again.\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
				"Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "Progress: ['pink block in the brown box']. Remaining goals: ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
				"Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['pink block and gray block in the brown box']. Remaining goals: ['Put the gray block, cyan block, and gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink and gray blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the pink and gray blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the pink and gray blocks are not in the brown box; the current progress is ['gray block in the brown box']. The task feasibility is unaffected since the remaining target objects [pink block, gray block, cyan block, gray block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the pink and gray blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['pink block and gray block in the brown box']. To address the anomaly, the remaining goal is ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['pink block, gray block, and gray block in the brown box']. Remaining goals: ['Put cyan and gray blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink, gray, and gray blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the pink, gray, and gray blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the pink, gray, and gray blocks are not in the brown box; the current progress is ['cyan block in the brown box']. The task feasibility is unaffected since the remaining target objects [pink block, gray block, gray block, gray block] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the pink, gray, and gray blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['pink block and cyan block in the brown box']. To address the anomaly, the remaining goal is ['Put the gray and gray blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['pink block, gray block, and cyan block in the brown box']. To address the anomaly, the remaining goal is ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['pink block, gray block, gray block, and cyan block are in the brown box']. Remaining goals: ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
				"Progress: ['pink block, gray block, gray block, and cyan block in the brown box']. Remaining goals: ['Put the gray block in the brown box'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['pink block, gray block, gray block, cyan block, and gray block in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
                )
            anomaly_episode_list=[episode_1,episode_2]
        elif anomaly_type=="removal":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, cyan, red, red, pink, yellow, and purple blocks; there is a brown box and a trash can. The instruction is 'please put all cyan, pink, and red blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, pink block, cyan block, red block, red block, and pink block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A cyan block is in the brown box']. Remaining goals: ['Put the pink block, cyan block, red block, red block, and pink block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"
                "### User:\n"+
                "The action succeeded, and a red block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a red block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A cyan block and a pink block are in the brown box'] is unaffected; the task feasibility is affected since the disappeared red block is among the remaining target objects [cyan block, red block, red block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n" )
            
            episode_2=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, pink, white, gray, and green blocks; there is a brown box and a trash can. The instruction is 'please put all cyan, pink, and white blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, pink block, pink block, and white block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A cyan block is in the brown box']. Remaining goals: ['Put the pink block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a green block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a green block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A cyan block and a pink block are in the brown box'] is unaffected; the task feasibility is unaffected since the disappeared green block is not among the remaining target objects [pink block, white block].\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block, pink block, and pink block are in the brown box']. Remaining goals: ['Put the white block in the brown box'].\n"+
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "Progress: ['cyan block, pink block, pink block, and white block are in the brown box']. All goals are completed.\n"+
                "### User:\n" +
                "What is your next plan?\n" +
				"### Assistant:\n"+
                "done.\n")

            episode_3=(
                "### User:\n"+
                "In the initial state, there are blue, pink, red, cyan, orange, and white blocks; there is a brown box and a trash can. The instruction is 'please put all blue, pink, red, and cyan blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Blue block, pink block, red block, and cyan block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A blue block is in the brown box']. Remaining goals: ['Put the pink block, red block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and an orange block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [an orange block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A blue block and a pink block are in the brown box'] is unaffected; the task feasibility is unaffected since the disappeared orange block is not among the remaining target objects [red block, cyan block].\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a cyan block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a cyan block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['blue block, pink block, and red block are in the brown box'] is unaffected; the task feasibility is affected since the disappeared cyan block is among the remaining target objects [cyan block].\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "The task feasibility is affected.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "alert.\n"
            )

            anomaly_episode_list=[episode_1,episode_2,episode_3]
    elif "pyramid" in task:
        if anomaly_type=="addition":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the red, blue, green, yellow, orange, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['red, blue, and green blocks make the bottom row; yellow and orange blocks make the middle row; pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['None of the rows built']. Remaining goals: ['put the red, blue, and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
				"### User:\n"+
				"What is your next plan?\n"+
				"### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
				"### User:\n"+
				"The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['red block on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears at the top right.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen purple block appears at the top right] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['red and blue blocks on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, orange block, pink block] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The robot will not be affected since the anomaly block [purple block at the top right] is not a target object and has a different color from any target blocks.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
                "### User:\n"+
                "The action failed, and a never-seen pink block appears at the bottom left.\n"+
				"### User:\n"
                "Analyze the effect of the anomaly [a never-seen pink block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['bottom row (red, blue, and green blocks) is built'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, orange block, pink bowl] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The robot may mistake the anomaly block [pink block at the bottom left] for the target pink block since they have the same color.\n" +
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion.\n" +
                "### User:\n"
                "What is your next plan?\n" +
                "### Assistant:\n"
                "put the pink block at the bottom left into the trash can and attempt the yellow block again.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
				"### User:\n"+
				"Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks) is built, and yellow block is on top of the bottom row']. Remaining goals: ['put the orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+                
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks) and middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top right.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen gray block appears at the top right] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['bottom row (red, blue, and green blocks), middle row (yellow and orange blocks), and top row (the pink block) are built'] is unaffected; the task feasibility is unaffected since there is no target object left and all goals are completed.\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected since the anomaly block [gray block appears at the top right] is not a target object and all goals are completed.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")

            episode_2=(
                "### User:\n"+
                "In the initial state, there are blue, green, yellow, red, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, green, yellow, red, orange, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['blue, green, and yellow blocks make the bottom row; red and orange blocks make the middle row; pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray block appears at the top left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['blue block on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, red block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [gray block at the top left] is not a target object and has a different color from any target blocks.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "Progress: ['blue block on the stand']. Remaining goals: ['put the green and yellow blocks on the stand to make the bottom row'; 'put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the middle brown block of the stand.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue and green blocks on the stand']. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and a never-seen red block appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['blue and green blocks on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, red block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [red block at the bottom right] for the target red block since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block at the bottom right into the trash can and attempt the yellow block again.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['blue and green blocks on the stand']. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the darkest brown block of the stand.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['bottom row (blue, green, and yellow blocks) is built']. Remaining goals: ['put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row']\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The bottom row (blue, green, and yellow blocks) is built, and the red block is on top of the bottom row'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [pink block at the top right] for the target pink block since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['bottom row (blue, green, and yellow blocks) is built, and red block is on top of the bottom row']. Remaining goals: ['put the orange block on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the green and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, green, and yellow blocks) and middle row (red and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, green, and yellow blocks), middle row (red and orange blocks), and top row (pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_3=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, green, orange, white, and pink blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the yellow, blue, red, green, orange, and white blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['yellow, blue, and red blocks make the bottom row; green and orange blocks make the middle row; white block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['yellow block on the stand']. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen cyan block appears in the darkest brown block of the stand.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen cyan block appears in the darkest brown block of the stand] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['yellow and blue blocks on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, green block, orange block, white block] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The anomaly block [cyan block on the darkest brown block of the stand] takes the expected position of the target red block, and the robot may not find a space to put the target red block to make the bottom row.\n"+
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion.\n" +
                "### User:\n"
                "What is your next plan?\n" +
                "### Assistant:\n"
                "put the cyan block on the darkest brown block of the stand into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['yellow and blue blocks on the stand']. Remaining goals: ['put the red block on the stand to make the bottom row'; 'put the green and orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the yellow and blue blocks.\n"+
                "### User:\n"+
                "The action failed, and a never-seen pink block is placed on the blue and red blocks.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen pink block is placed on the blue and red blocks] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['bottom row (yellow, blue, and red blocks) is built'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, orange block, white block] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The anomaly block [pink block on the blue and red blocks] takes the expected position of the target orange block, and the robot may not find a space to put the target orange block to make the middle row.\n"+
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion and attempt the green block again.\n" +
                "### User:\n"
                "What is your next plan?\n" +
                "### Assistant:\n"
                "put the pink block on the blue and red blocks into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the green block on the yellow and blue blocks.\n"+
				"### User:\n"+
				"The action succeeded, and no anomaly happened.\n"+
				"### User:\n"
                "Please describe the progress and the remaining goals.\n" +
				"### Assistant:\n"+
				"Progress: ['bottom row (yellow, blue, and red blocks) is built, and green block is on top of the bottom row']. Remaining goals: ['put the orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and red blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (yellow, blue, and red blocks) and middle row (green and orange blocks) are built']. Remaining goals: ['put the white block on the middle row to make the top row'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the green and orange blocks.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
				"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (yellow, blue, and red blocks) and middle row (green and orange blocks) are built']. Remaining goals: ['put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the green and orange blocks.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (yellow, blue, and red blocks), middle row (green and orange blocks), top row (white block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            
            episode_4=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the red, blue, green, yellow, orange, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['red, blue, and green blocks make the bottom row; yellow and orange blocks make the middle row; pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears on the middle brown block of the stand.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple block appears on the middle brown block of the stand] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['red block on the stand'] is unaffected; the task feasibility is affected since the remaining target objects [blue block, green block, yellow block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [purple block on the middle brown block of the stand] takes the expected position of the target blue block, and the robot may not find a space to put the target blue block to make the bottom row.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block on the middle brown block of the stand into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['red block on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
		        "### Assistant:\n"+
		        "Progress: ['red block on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['red and blue blocks on the stand']. Remaining goals: ['put the green block on the darkest brown block of the stand to make the bottom row'; 'put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and a never-seen red block is placed on the red and blue blocks.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block is placed on the red and blue blocks] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['red and blue blocks on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [red block on the red and blue blocks] takes the expected position of the target yellow block, and the robot may not find a space to put the target yellow block to make the middle row.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the red and blue blocks into the trash can and attempt the green block again.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['red and blue blocks on the stand']. Remaining goals: ['put the green block on the darkest brown block of the stand to complete the bottom row'; 'put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed on the blue and green blocks.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears on the blue and green blocks] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['yellow block is on top of the built bottom row (red, blue, and green blocks)'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [pink block on the blue and green blocks] takes the expected position of the target orange block, and the robot may not find a space to put the target orange block to make the middle row.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the blue and green blocks into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['bottom row (red, blue, and green blocks) is built, and yellow block is on top of the bottom row']. Remaining goals: ['put the orange block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks) and middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (red, blue, and green blocks), middle row (yellow and orange blocks), and top row (pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )


            episode_5=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, gray, white, green, orange, and yellow blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the cyan, pink, gray, white, green, and orange blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['cyan, pink, and gray blocks make the bottom row; white and green blocks make the middle row; orange block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan block on the stand']. Remaining goals: ['put the pink and gray blocks on the stand to make the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['cyan and pink blocks on the stand']. Remaining goals: ['put the gray block on the darkest brown block of the stand to complete the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and a never-seen stand appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen stand appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['cyan and pink blocks are on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [gray block, white block, green block, orange block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly stand [stand at the top right] as the target stand since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly stand to prevent confusion and attempt the gray block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the stand at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['cyan and pink blocks on the stand']. Remaining goals: ['put the gray block on the darkest brown block of the stand to complete the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (cyan, pink, and gray blocks) is built']. Remaining goals: ['put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the cyan and pink blocks.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
              	"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
		        "Progress: ['bottom row (cyan, pink, and gray blocks) is built']. Remaining goals: ['put the white block and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the cyan and pink blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (cyan, pink, and gray blocks) is built, and white block is on top of the bottom row']. Remaining goals: ['put the green block on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the pink and gray blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (cyan, pink, and gray blocks) and middle row (white and green blocks) are built']. Remaining goals: ['put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the white and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (cyan, pink, and gray blocks), middle row (white and green blocks), and top row (orange block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
        elif anomaly_type=="removal":
            episode_1 = (
                "### User:\n" +
                "In the initial state, there are red, green, blue, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the red, green, blue, yellow, orange, and pink blocks'\n"+
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Goal state: ['red, green, and blue blocks make the bottom row; yellow and orange blocks make the middle row; pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['red block on the stand']. Remaining goals: ['Put the green and blue blocks on the stand to make the bottom row'; 'Put the yellow and orange blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly ['orange block on the table disappears'] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['red and green blocks on the stand'] is unaffected; the task feasibility is unaffected since the disappeared orange block is among the remaining target objects [blue block, yellow block, orange block, pink block].\n" 
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert since the task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            episode_2 = (
                "### User:\n" +
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, purple, and pink blocks'\n"+
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Goal state: ['blue, yellow, and green blocks make the bottom row; red and purple blocks make the middle row; pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['blue block on the stand']. Remaining goals: ['Put the yellow and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the yellow block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly ['orange block on the table disappears'] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['blue block and yellow block on the stand'] is unaffected; the task feasibility is unaffected since the disappeared orange block is not among the remaining target objects [green block, red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block on the darkest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block on the blue and yellow blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['bottom row (blue, yellow, and green blocks) and middle row (red block) are built']. Remaining goals: ['Put the purple block on the middle row to complete it'; 'Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the purple block on the yellow and green blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['bottom row (blue, yellow, and green blocks) and middle row (red and purple blocks) are built']. Remaining goals: ['Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the pink block on the red and purple blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['bottom row (blue, yellow, and green blocks), middle row (red and purple blocks), and top row (pink block) are built']. All goals are completed.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "done.\n"
            )

            episode_3 = (
                "### User:\n" +
                "In the initial state, there are cyan, white, green, red, purple, pink, yellow, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the cyan, white, green, red, purple, and pink blocks'\n"+
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Goal state: ['cyan, white, and green blocks make the bottom row; red and purple blocks make the middle row; pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the cyan block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "Progress: ['cyan block on the stand']. Remaining goals: ['Put the white and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the white block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the yellow block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['cyan block and a white block on the stand'] is unaffected; the task feasibility is unaffected since the disappeared yellow block is not among the remaining target objects [green block, red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block on the darkest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the purple block on table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the purple block on table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['bottom row (blue, yellow, and green blocks) is built'] is unaffected; the task feasibility is affected since the disappeared purple block is among the remaining target objects [red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert since the task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3]
        elif anomaly_type=="displacement":
            episode_1 = (
                "### User:\n"+
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and brown blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, purple, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['blue, yellow, and green blocks make the bottom row; red and purple blocks make the middle row; pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
				"### User:\n"+
				"The action failed, and no anomaly happened.\n"+
				"### User:\n"+
				"Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"Progress: ['None of the rows built']. Remaining goals: ['put the blue, yellow, and green blocks on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
				"### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
				"### User:\n"+
				"The action succeeded, and no anomaly happened.\n"+
				"### Assistant:\n"+
				"Progress: ['blue block on the stand']. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
				"### User:\n"+
				"What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and the blue block on the stand is moved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the blue block on the stand moved to another position on the table.] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the blue block used to make the bottom row is moved to another position on the table. The current progress is ['yellow block on the middle brown block of the stand']; the task feasibility is unaffected since the remaining target objects [blue block, green block, red block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the blue block back to the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['blue and yellow blocks on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action failed, and the green block on the stand is moved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the green block on the stand is moved to another position on the table.] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the green block used to make the bottom row is moved to another position on the table. The current progress is ['blue and yellow blocks on the stand']; the task feasibility is unaffected since the remaining target objects [red block, green block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the green block back to the stand to resume the progress and attempt the red block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red block on the blue and yellow blocks'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
		"### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
		"### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['bottom row (blue, yellow, and green blocks) is built, and red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
               	"### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) and middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks), middle row (red and purple blocks), and top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_2 = (
                "### User:\n"+
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and brown blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, purple, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Goal state: ['blue, yellow, and green blocks make the bottom row; red and purple blocks make the middle row; pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue block on the stand']. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue and yellow blocks on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action failed, and the blue and yellow blocks on the stand are moved to other positions of the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the blue and yellow blocks on the stand are moved to other positions of the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the blue and yellow blocks used to make the bottom row are moved to other positions. The current progress is ['None of the rows built']; the task feasibility is unaffected since the remaining target objects [blue block, yellow block, green block, red block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the blue and yellow blocks back to the stand to resume the progress and attempt the green block again.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue block on the stand']. To address this anomaly, the remaining goal is ['put the yellow block on the middle brown block of the stand and put the green block on the darkest brown block of the stand. '].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['blue and yellow blocks on the stand']. Remaining goals: ['put the green block on the darkest brown block of the stand.'].\n"+
				"### User:\n"+
                "What is your next plan?\n"+
				"### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
				"The anomaly has been addressed. Progress: ['bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) is built, and red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) and middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action failed, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
				"### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks) and middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
				"### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['bottom row (blue, yellow, and green blocks), middle row (red and purple blocks), and top row (pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2]
        
        
    return anomaly_episode_list    