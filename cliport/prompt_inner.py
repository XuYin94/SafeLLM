import random

def get_help_infomation(task):
    if "matching" in task:
        please_help = (
            "The instruction is 'put current-seen blocks in bowls with matching colors'.\n" +
            "Before providing the action plan, please define the final goal state. Note that you should explicitly verify and state the matching pairs, ensuring your planned blocks and bowls have matching colors and are present in the initial state to avoid missing or incorrect pairs.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]' and that each step matches the color of the block to the color of the bowl.")
            #    "Ensure each step matches the color of the block to the color of the bowl.\n"
            #    "Explicitly verify and state the matching pairs and check if your planned blocks and bowls are present before estimating the goal state to avoid missing or wrong pairs.")
    elif "box" in task:
        please_help = (
            "The instruction is 'put current-seen blocks in the brown box'.\n" +
            "Before providing the action plan, please define the final goal state.\n"+
            "For the planned action steps, ensure each action follows the format 'put the [object1] in the [object2]'.")
    else:
        please_help=(
            "The instruction is 'Put blocks together to form a three-row pyramid'. \n"+
            "Before providing the action plan, please define the final goal state by specifying which blocks should be placed on the bottom, middle, and top rows.\n" +
            "For the planned action steps, ensure each action follows the format 'put the [object1] on the [object2]'.")
    return please_help


def get_inner_prompt(task, anomaly_type="pick"):
    please_help=get_help_infomation(task)
   
    if anomaly_type=="None":
        episode_list=get_normal_execution(task=task)[:5]
    else:
        episode_list=get_normal_execution(task=task)[:5]
        episode_list+=get_handling_prompt(task=task,anomaly_type=anomaly_type)
    
    random.shuffle(episode_list)
    print(len(episode_list))
        
    episode_list='\n'.join(episode_list)
    episode_list+="\n"
    system_prompt = ("You are a helpful assistant capable of decomposing high-level human instructions into low-level executable actions. In addition, you should analyze scene feedback to identify any anomaly conditions and provide appropriate corrective actions. For each task, break down the instructions into detailed steps and suggest corrective actions to address the issues if any anomalies are detected based on the scene feedback.\n")
    system_prompt+=please_help
    return please_help, episode_list, system_prompt

def get_normal_execution(task):
    
    if "-matching-bowl" in task:
        example_1 = ("### User:\n"+
                    "In the initial state, there are green, red, purple, and yellow blocks; there are green, red, purple, cyan, and blue bowls; and a trash can.\n"+
                    ##"{please_help}\n"+
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
                    "The final goal state is ['Green, red, and purple blocks are in their corresponding bowls'].\n"+          
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n" +
                    "### User:\n"+
                    'The action succeeded, and no anomaly happened.\n'+
                    "### User:\n"+
                    'Please describe the progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the red and purple blocks in their corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe The progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green and red blocks are in their corresponding bowls']. The remaining goal is ['put the purple block in its corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the purple block in the purple bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe The progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green, red and purple blocks are in their corresponding bowls']. All goals are completed.\n" +
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "done.\n"
                    )
        
        example_2 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, and orange bowls; and a trash can.\n" +
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The final goal state is ['Yellow, blue, and orange blocks are in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n" +
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue and orange blocks in their corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow, blue, and orange blocks are in their corresponding bowls.']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n") 
        
        example_3 = ("### User:\n"+
                    "In the initial state, there are white, red, pink, and green blocks; there are white, red, pink, yellow, and cyan bowls; and a trash can.\n" +
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The goal state is ['White, red, and pink blocks are in the corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the red and pink blocks in their corresponding bowls'].\n"+
                    "### User:\n"+"What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white and red blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'.]\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, red, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan? \n"+
                    "### Assistant:\n"+
                    "done.\n")
                    
        example_4 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, orange, red, and white bowls; and a trash can.\n"+ 
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
                    "The final goal state is ['Yellow, blue, and orange blocks are in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow, blue, and orange blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_5 = ("### User:\n"+
                    "In the initial state, there are white, green, yellow, orange, blue, and pink blocks; there are white, green, yellow, orange, and purple bowls; and a trash can.\n"+
                    #"{please_help}\n"+
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
		            "The final goal state is ['White, green, yellow, and orange blocks are in their corresponding bowls'].\n"+                   
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the green, yellow, and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white and green blocks are in their corresponding bowls']. The remaining goal is ['put the yellow and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+"put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, green, and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, green, yellow, and orange blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your next plan?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_6=(
            "### User:\n"+
            "In the initial state, there are white, blue, yellow, green, pink, and red blocks; there are white, blue, yellow, orange, cyan, and purple bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['White, blue, and yellow blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block in the white bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the blue and yellow blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white and blue blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white, blue, and yellow blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_7=(
            "### User:\n"+ 
            "In the initial state, there are red, green, blue, cyan, pink, and orange blocks; there are red, green, blue, cyan, yellow, and purple blocks; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Red, green, blue, and cyan blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red block is in its corresponding bowl']. The remaining goal is ['put the green, blue, and cyan blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue and cyan blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red, green, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the cyan block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the cyan block in the cyan bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red, green, blue, and cyan blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_8=(
            "### User:\n"+
            "In the initial state, there are purple, yellow, green, blue, white, and red blocks; there are purple, yellow, green, blue, orange, and pink bowls; and a trash can.\n"+
            #"{please_help}\n"+ 
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Purple, yellow, green, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the purple block in the purple bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple block is in its corresponding bowl']. The remaining goal is ['put the yellow, green, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the green and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple, yellow, and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple, yellow, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
            
        )
        example_9=(
            "### User:\n"+ 
            "In the initial state, there are orange, red, green, blue, pink, and cyan blocks; there are orange, red, green, blue, purple, and yellow bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Orange, red, green, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the orange bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange block is in its corresponding bowl']. The remaining goal is ['put the red, green, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange and red blocks are in their corresponding bowls']. The remaining goal is ['put the green and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange, red, and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange, red, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_10=(
            "### User:\n"+ 
            "In the initial state, there are yellow, green, red, blue, orange, and purple blocks; there are yellow, green, red, blue, pink, and cyan bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Yellow, green, red, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the green, red, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow and green blocks are in their corresponding bowls']. The remaining goal is ['put the red and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow, green, and red blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow, green, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[example_1,example_2,example_3,example_4,example_5,example_6,example_7,example_8,example_9,example_10]
    
    elif task=="packing-boxes":
        episode_1=(
            "### User:\n"+
            "In the initial state, there are red, blue, red, green, blue, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, blue, and green blocks in the brown box'.\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Red block, blue block, red block, green block, and blue block are in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['A red block is in the brown box']. Remaining goals: ['Put blue block, red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['A red block and a blue block are in the brown box']. Remaining goals: ['Put red block, green block, and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Red block, blue block, and red block are in the brown box']. Remaining goals: ['Put green block and blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Red block, blue block, red block, and green block are in the brown box']. Remaining goals: ['Put the blue block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### Assistant:\n"+
            "Progress: ['Red block, blue block, red block, green block, and blue block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_2=(
            "### User:\n"+
            "In the initial state, there are orange, pink, orange, cyan, orange, pink, green, and gray blocks; there is a brown box and a trash can. The instruction is 'Please put the orange, pink and cyan blocks in the brown box'.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Orange block, pink block, orange block, cyan block, orange block, and pink block are in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['An orange block is in the brown box']. Remaining goals: ['Put pink block, orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['An orange block and a pink block are in the brown box']. Remaining goals: ['Put orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Orange block, pink block, and orange block are in the brown box']. Remaining goals: ['Put cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the cyan block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Orange block, pink block, orange block, and cyan block are in the brown box']. Remaining goals: ['Put orange block and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Orange block, pink block, orange block, cyan block, and orange block are in the brown box']. Remaining goals: ['Put the pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Orange block, pink block, orange block, cyan block, orange block, and pink block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_3=("### User:\n"+
            "In the initial state, there are blue, gray, blue, green, white, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all blue, gray and green blocks in the brown box'.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Blue block, gray block, blue block, and green block are in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['A blue block is in the brown box']. Remaining goals: ['Put gray block, blue block, and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['A blue block and a gray block are in the brown box']. Remaining goals: ['Put blue block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Blue block, gray block, and blue block are in the brown box']. Remaining goals: ['Put green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Blue block, gray block, blue block, and green block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")

        episode_4=("### User:\n"+
            "In the initial state, there are red, red, green, gray, green, and purple blocks; there is a brown box and a trash can. The instruction is 'Please put all red, green, and gray blocks in the brown box'.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Red block, red block, green block, gray block, and green block are in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['A red block is in the brown box']. Remaining goals: ['Put blue block, green block, yellow block, orange block, and purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Two red blocks are in the brown box']. Remaining goals: ['Put green block, gray block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Two red blocks and green block are in the brown box']. Remaining goals: ['Put gray block and green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Two red blocks, green block and gray block are in the brown box']. Remaining goals: ['Put the green block in the brown box'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: ['Red block, red block, green block, gray block, and green block are in the brown box']. All goals are completed.\n"+
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
            "Final goal state: ['the gray, red, and blue blocks make the bottom row; the brown and white blocks make the middle row; the pink block makes the top row'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a gray block is on the stand]. Remaining goals: ['put the red and blue blocks on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The gray and red blocks are on the stand]. Remaining goals: ['put the blue block on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, red, and blue blocks) is built]. Remaining goals: ['put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the gray and red blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, red, and blue blocks) is built, and the brown block is on top of the bottom row]. Remaining goals: ['put the white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the red and blue blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, red, and blue blocks) and the middle row (brown and white blocks) are built]. Remaining goals: ['put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the brown and white blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, red, and blue blocks), the middle row (brown and white blocks), and the top row (the pink block) are built]. All goals are completed\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n")
		
        episode_2 = (
            "### User:\n" +
            "In the initial state, there are yellow, blue, red, orange, green, brown, pink, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the yellow, blue, red, orange, green and brown blocks'\n"+
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Final goal state: ['the yellow, blue, and red blocks make the bottom row; the orange and green blocks make in the middle row; the brown block makes the top row'].\n" +
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the yellow block on the lightest brown block of the stand.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a yellow block is on the stand]. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the blue block on the middle brown block of the stand.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The yellow and blue blocks are on the stand]. Remaining goals: ['put the red block on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (yellow, blue, and red blocks) is built]. Remaining goals: ['put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "put the orange block on the yellow and blue blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (yellow, blue, and red blocks) is built, the orange block is on top of the bottom row]. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the green block on the blue and red blocks.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (yellow, blue, and red blocks) and the middle row (orange and green blocks) are built]. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the brown block on the orange and green blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n" +
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (yellow, blue, and red blocks), the middle row (orange and green blocks), and the top row (the brown block) are built]. All goals are completed\n"+
            "### User:\n" +
            "What is your next plan?\n" +
            "### Assistant:\n" +
            "done.\n")
        
        episode_3=(
            "### User:\n" +
            "In the initial state, there are orange, purple, white, green, yellow, brown, and pink blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the orange, purple, white, green, yellow, and brown blocks'\n"+
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Final goal state: ['the orange, purple, and white blocks make the bottom row; the green and yellow blocks make the middle row; the brown block makes the top row'].\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the orange block on the lightest brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [an orange block is on the stand]. Remaining goals: ['put the purple and white blocks on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the purple block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The orange and purple blocks are on the stand]. Remaining goals: ['put the white block on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (orange, purple, and white blocks) is built]. Remaining goals: ['put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the orange and purple blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (orange, purple, and white blocks) is built, and the green block is on top of the bottom row]. Remaining goals: ['put the yellow block on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the purple and white blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (orange, purple, and white blocks) and the middle row (green and yellow blocks) are built]. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the brown block on the purple and brown blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (orange, purple, and white blocks), the middle row (green and yellow blocks), and the top row (the brown block) are built]. All goals are completed\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "done.\n")
        
        episode_4=(
            "### User:\n" +
            "In the initial state, there are gray, pink, yellow, red, green, blue, and purple blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the gray, pink, yellow, red, green, and blue blocks'\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Final goal state: ['the gray, pink, and yellow blocks make bottom row; the red and green blocks make the middle row; the blue block makes the top row'].\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a gray block is on the stand]. Remaining goals: ['put the pink and yellow blocks on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the pink block on the middle brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The gray and pink blocks are on the stand]. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the yellow block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: [The bottom row (gray, pink, and yellow blocks) is built]. Remaining goals: ['put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n" +
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the gray and pink blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n" +
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, pink, and yellow blocks) is built, and red block is on top of the bottom row]. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the green block on the pink and yellow blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, pink, and yellow blocks) and the middle row (red and green blocks) are built]. Remaining goals: ['put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the blue block on the red and green blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: [The bottom (gray, pink, and yellow blocks), the middle row (red and green blocks), and the top row (the blue block) are built]. All goals are completed\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )

        episode_5=(
            "### User:\n" +
            "In the initial state, there are blue, yellow, green, red, white, pink, and orange blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, white, and pink blocks'\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and white blocks make the middle row; the pink block makes the top row'].\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the blue block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a blue block is on the stand]. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the yellow block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The blue and yellow blocks are on the stand]. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and white blocks on  top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (blue, yellow, and green blocks) is built]. Remaining goals: ['put the red and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the red block on the blue and yellow blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row]. Remaining goals: ['put the white block on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "put the white block on the yellow and green blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (blue, yellow, and green blocks) and the middle row (red and white blocks) are built]. Remaining goals: ['put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n" +
            "put the pink block on the red and white blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (blue, yellow, and green blocks), the middle row (red and white blocks), and the top row (the pink block) are built]. All goals are completed\n"+
            "### User:\n"+
            "What is your next plan?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
    return episode_list 
    
    
def get_handling_prompt(task, anomaly_type="pick"):
    if "-matching-bowl" in task:
        if anomaly_type=="removal":
            episode_1=(
                "### User:\n" +
                "In the initial state, there are gray, red, blue, brown, and white blocks; there are gray, red, blue, and yellow bowls; and a trash can.\n" +
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The final goal state is ['Gray, red, and blue blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the gray block in the gray bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the white block on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block in the red bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the blue block on the table disappears.\n" +
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
                "The final goal state is ['Pink, cyan, yellow, and blue blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the pink block in the pink bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the brown bowl on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the cyan block in the cyan bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the blue bowl on the table disappears.\n" +
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
                "The final goal state is ['Blue, green, red, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the white block on the table disappears.\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow bowl on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            
            episode_4=(
                "### User:\n" +
                "In the initial state, there are blue, green, red, yellow, purple,  white, and brown blocks; there are blue, green, red, yellow, orange, and pink bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "The final goal state is ['Blue, green, red, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block in the blue bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the purple block on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the pink bowl on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your next plan?\n" +
                "### Assistant:\n"+
                "put the red block in the red bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe The progress and the remaining goals.\n'+
                "### Assistant:\n"+
                "The progress is ['the blue, green, and red blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowls'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe The progress and the remaining goals.\n'+
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
                "The final goal state is ['Green, pink, and yellow blocks are in their corresponding bowls'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block in the green bowl.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow block on the table disappears.\n" +
                "### User:\n"+
                "How to handle this anomaly?\n"+
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
                "The final goal state is ['Cyan, yellow, orange, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan block is in its corresponding bowl']. The remaining goal is ['put the yellow, orange, and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the orange and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the cyan and yellow blocks in their corresponding bowls are moved to other positions on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the cyan and yellow blocks back to their corresponding bowls.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the cyan and orange blocks are in their corresponding bowls']. To address this anomaly, the remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the cyan, yellow, and orange blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan, yellow, orange, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_2=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, pink, gray, and green blocks; there are yellow, blue, red, pink, and purple bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Yellow, blue, red, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue, red, and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the red and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the yellow and blue blocks in their corresponding bowls are moved to other positions on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the yellow and blue blocks back to their corresponding bowls.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the red and yellow blocks are in their corresponding bowls']. To address this anomaly, the remaining goal is ['put the blue block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red, yellow, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, yellow, blue, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
                )
            episode_3=(
                "### User:\n"+
                "In the initial state, there are red, green, blue, yellow, pink, and white blocks; there are red, green, blue, yellow, and orange bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Red, green, blue, and yellow blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red block is in its corresponding bowl']. The remaining goal is ['put the green, blue, and yellow blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the red block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the red block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red and green blocks are in their corresponding bowls']; the remaining goal is ['put the blue and yellow blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, green, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, green, blue, and yellow blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_4=(
                "### User:\n"+
                "In the initial state, there are green, blue, pink, orange, red, and purple blocks; there are green, blue, pink, yellow, and white bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Green, blue, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the blue and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the green block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the green block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The achieved progress is ['the green and blue blocks are in their corresponding bowls']; the remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, blue, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            episode_5=(
                "### User:\n"+
                "In the initial state, there are brown, blue, green, red, yellow, and pink blocks; there are brown, blue, green, and purple bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Brown, blue, and green blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the brown block in the brown bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the brown block is in its corresponding bowl']. The remaining goal is ['put the blue and green blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the brown and blue blocks are in their corresponding bowls']. The remaining goal is ['put the green block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the brown block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the brown block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the brown block in the brown bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the brown, blue, and green blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
        
        elif anomaly_type=="addition":
            episode_1=(
                        "### User:\n"+
                        "In the initial state, there are blue, pink, red, purple, and white blocks; there are blue, pink, red, purple, yellow and cyan bowls; and a trash can.\n"+
                        "What is the final goal state?\n"+
                        "### Assistant:\n"+
                        "The initial state contains the following pairs of blocks and matching bowls: Blue block -> Blue bowl, Pink block -> Pink bowl, Red block -> Red bowl, Purple block -> Purple bowl. The white block does not have a corresponding bowl, and the yellow and cyan bowls do not have corresponding blocks. The final goal state is ['Blue, pink, red, and purple blocks are in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "put the blue block in the blue bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe the progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the blue block is in its corresponding bowl']. The remaining goal is ['put the pink, red, and purple blocks in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "put the pink block in the pink bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen red block appears at the bottom right.\n"+
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
                        "The anomaly has been addressed. The progress is ['the blue and pink blocks are in their corresponding bowls']. The remaining goal is ['put the red and purple block in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "put the red block in the red bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen purple block appears at the top right.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "Remove the anomaly block to prevent confusion.\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "put the purple block at the top right into the trash can.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe the progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The anomaly has been addressed. The progress is ['the blue, pink, and red blocks are in their corresponding bowls']. The remaining goal is ['put the purple block in its corresponding bowl'].\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "put the purple block in the purple bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe the progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the blue, pink, red, and purple blocks are in their corresponding bowls']. All goals are completed.\n"+
                        "### User:\n"+
                        "What is your next plan?\n"+
                        "### Assistant:\n"+
                        "done.\n")
            
            episode_2=(
                        "### User:\n"+
                        "In the initial state, there are green, yellow, red, blue, white, and cyan blocks; there are green, yellow, red, blue, and orange bowls; and a trash can.\n" +
                        "What is the final goal state?\n" +
                        "### Assistant:\n" +
                        "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl. The white and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. The final goal state is ['Green, yellow, red, and blue blocks are in their corresponding bowls'].\n" +
                        "### User:\n" +
                        "What is your next plan?\n" +
                        "### Assistant:\n" +
                        "put the green block in the green bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and a never-seen white block appears at the bottom left.\n" +
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
                        "The progress is ['the green and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the red and blue blocks in their corresponding bowls'].\n"+
                        "### User:\n" +
                        "What is your next plan?\n" +
                        "### Assistant:\n" +
                        "put the red block in the red bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and a never-seen cyan block appears at the bottom left.\n" +
                        "### User:\n" +
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n" +
                        "No action needed\n" +
                        "### User:\n" +
                        "What is your next plan?\n" +
                        "### Assistant:\n" +
                        "put the blue block in the blue bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and no anomaly happened.\n" +
                        "### User:\n" +
                        "Please describe the progress and the remaining goals.\n" +
                        "### Assistant:\n" +
                        "The progress is ['the green, yellow, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n" +
                        "### User:\n" +
                        "What is your next plan?\n" +
                        "### Assistant:\n" +
                        "done.\n"
            )

            ## address the perturbation when the added block in the non-target bowls
            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, white, cyan, green, and yellow blocks; there are bowls with orange, white, cyan, and gray bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Orange block -> Orange bowl, White block -> White bowl, Cyan block -> Cyan bowl. The green and yellow blocks do not have corresponding bowls, and the gray bowl does not have a corresponding block. The final goal state is ['Orange, cyan, and white blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block is placed into the white bowl.\n"+
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
                "The anomaly has been addressed. The progress is ['the orange block is in its corresponding bowl']. The remaining goal is ['put the white and cyan blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the white bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed into the cyan bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
		        "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the cyan bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the orange and white blocks are in their corresponding bowls']. The remaining goal is ['put the cyan block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the orange, white, and cyan blocks are in their corresponding bowls']. All goals are completed.\n"+
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
                "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl. The green and orange blocks do not have corresponding bowls, and the purple and cyan bowls do not have corresponding blocks. The final goal state is ['Yellow, red, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen cyan block is placed into the purple bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen green block appears in the cyan bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            ## address the perturbation when the addition is the bowl
            episode_5=(
                "### User:\n"+
                "In the initial state, there are green, pink, gray, red, blue, and cyan blocks; there are green, pink, gray, and orange bowls; and a trash can.\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Pink block -> Pink bowl, Gray block -> Gray bowl. The red, blue, and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. The final goal state is ['Green, pink, and gray blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink bowl appears at the bottom right.\n"+
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
                "The anomaly has been addressed. The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the pink and gray blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray bowl appears at the bottom left.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray bowl at the bottom left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the green block and pink blocks are in their corresponding bowls']. The remaining goal is ['put the gray block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, pink, and gray blocks are in their corresponding bowls']. All goals are completed.\n"+
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
                "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Red block -> Red bowl, Pink block -> Pink bowl. The gray and green blocks do not have their corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Yellow, blue, red, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue, red, and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen green bowl appears at the bottom left.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
		        "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple bowl appears at the bottom right.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow, blue, red, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
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
                "The final goal state is ['Red block, red block, green block, yellow block, and orange block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A red block is in the brown box']. Remaining goals: ['Put the red block, green block, yellow block, and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears at the top left.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['two red blocks are in the brown box']. Remaining goals: ['Put the green block, yellow block, orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['two red blocks and one green block are in the brown box']. Remaining goals: ['Put the yellow block and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Red block, red block, green block, yellow block, and orange block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")

            episode_2=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, cyan, pink, white, red, yellow, and orange blocks; there is a brown box and a trash can. The instruction is 'please put all cyan, pink, and white blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, pink block, cyan block, pink block, and white block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A cyan block is in the brown box']. Remaining Goals: ['Put the pink block, cyan block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A cyan block and a pink block are in the brown box']. Remaining Goals: ['Put the cyan block, pink block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears at the top right.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Cyan block, pink block, cyan block, and pink block are in the brown box']. Remaining Goals: ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Cyan block, pink block, cyan block, pink block, and white block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n")
            
            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, purple, white, white, gray, pink, and green blocks; there is a brown box and a trash can. The instruction is 'please put all orange, purple, and white blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Orange block, purple block, white block, and white block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['An orange block is in the brown box']. Remaining Goals: ['Put the purple block, white block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears in the brown box.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Orange block and purple block are in the brown box']. Remaining Goals: ['Put the white and white blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Orange block, purple block, and white block are in the brown box']. Remaining Goals: ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Orange block, purple block, white block, and white block are in the brown box']. All goals are completed.\n"+
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
                "The final goal state is ['Gray block, blue block, gray block, cyan block, and cyan block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A gray block is in the brown box']. Remaining goals: ['Put the blue block, gray block, cyan block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A gray block and a blue block are in the brown box']. Remaining goals: ['Put the gray block, cyan block, and cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen brown box appears at the bottom right.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Remaining goals: ['Put the cyan and cyan blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Gray block, blue block, gray block, and cyan block are in the brown box']. Remaining goals: ['Put the cyan block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Gray block, blue block, gray block, cyan block, and cyan block are in the brown box']. All goals are completed.\n"+
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
                "The final goal state is ['Yellow block, red block, red block, blue block, and yellow block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A yellow block is in the brown box']. Remaining goals: ['Put the red block, red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A yellow block and a red block are in the brown box']. Remaining goals: ['Put the red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the yellow and red blocks in the brown box are moved to other positions on the table.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A yellow block and a red block are in the brown box']. Remaining goals: ['Put the red block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Yellow block, red block, and red block are in the brown box']. Remaining goals: ['Put the blue and yellow blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Yellow block, red block, orange block, and blue block are in the brown box']. Remaining goals: ['Put the yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Yellow block, red block, red block, blue block, and yellow block are in the brown box']. All goals are completed.\n"+
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
                "The final goal state is ['Pink block, gray block, gray block, cyan block, and gray block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A pink block is in the brown box']. Remaining goals: ['Put the gray block, gray block, cyan block, and gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A pink block and a gray block are in the brown box']. Remaining goals: ['Put the gray block, cyan block, and gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink and gray blocks in the brown box are moved to other positions on the table.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A pink block and a gray block are in the brown box']. To address the anomaly, the remaining goal is ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Pink block, gray block, and gray block are in the brown box']. Remaining goals: ['Put cyan and gray blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink, gray, and gray blocks in the brown box are moved to other positions on the table.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['A pink block and a cyan block are in the brown box']. To address the anomaly, the remaining goal is ['Put the gray and gray blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Pink block, gray block, and cyan block are in the brown box']. To address the anomaly, the remaining goal is ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Pink block, gray block, gray block, and cyan block are in the brown box']. Remaining goals: ['Put the gray block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Pink block, gray block, gray block, cyan block, and gray block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
                )

            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, purple, orange, red, red, purple, and yellow blocks; there is a brown box and a trash can. The instruction is 'please put all orange, red, and purple blocks in the brown box'.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Orange block, purple block, orange block, red block, red block, and purple block are in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['An orange block is in the brown box']. Remaining goals: ['Put the purple block, orange block, red block, red block, and purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['An orange block and a purple block are in the brown box']. Remaining goals: ['Put the orange block, red block, red block, and purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the orange and purple blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the orange and purple blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['two orange blocks are in the brown box']. To address the anomaly, the remaining goal is ['Put the purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Orange block, purple block, and orange block are in the brown box']. Remaining goals: ['Put the red block, red block, and purple blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the orange, purple, and orange blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the orange, purple, and orange blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['An orange block and a red block are in the brown box']. To address the anomaly, the remaining goal is ['Put the purple and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Orange block, purple block, and red block are in the brown box']. To address the anomaly, the remaining goal is ['Put the orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['Orange block, purple block, orange block, and red block are in the brown box']. Remaining goals: ['Put the red block and purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Orange block, purple block, orange block, red block, and red block are in the brown box']. Remaining goals: ['Put the purple block in the brown box']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['Orange block, purple block, orange block, red block, red block,and purple blocks are in the brown box']. All goals are completed\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3]
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
        if  anomaly_type=="addition":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the red, blue, green, yellow, orange, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the red, blue, and green blocks are in the bottom row; the yellow and orange blocks are in the middle row; the pink block is in the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a red block is on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears at the top right.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the bottom left.\n"+
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion.\n" +
                "### User:\n"
                "What is your next plan?\n" +
                "### Assistant:\n"
                "put the pink block at the bottom left into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The yellow block is on the built bottom row (red, blue, and green blocks)']. Remaining goals: ['put the orange block on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) and the middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top right.\n"+
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
                "Final goal state: ['the blue, green, and yellow blocks make the bottom row; the red and orange blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top left.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and green blocks are on the stand']. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block appears at the bottom right.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, green, and yellow blocks) is built']. Remaining goals: ['put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the top right.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, green, and yellow blocks) is built, and and the red block) is on top of the bottom row']. Remaining goals: ['put the orange block on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the green and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, green, and yellow blocks) and the middle row (red and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, green, and yellow blocks), the middle row (red and orange blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
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
                "Final goal state: ['the yellow, blue, and red blocks make the bottom row; the green and orange blocks make the middle row; the white block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a yellow block is on the stand']. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen cyan block appears in the darkest brown block of the stand.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen cyan block appears in the darkest brown block of the stand] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['The yellow and blue blocks are on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, green block, orange block, white block] are still available.\n" +
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
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The yellow and blue blocks are on the stand']. Remaining goals: ['put the red block on the stand to complete the bottom row'; 'put the green and orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the yellow and blue blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed on the blue and red blocks.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen pink block is placed on the blue and red blocks] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['The green block is on top of the built bottom row (yellow, blue, and red blocks)'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, white block] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The anomaly block [pink block on the blue and red blocks] takes the expected position of the target orange block, and the robot may not find a space to put the target orange block to make the middle row.\n"+
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion.\n" +
                "### User:\n"
                "What is your next plan?\n" +
                "### Assistant:\n"
                "put the pink block on the blue and red blocks into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The bottom row (yellow, blue, and red blocks) is built, and the green block is on top of the bottom row']. Remaining goals: ['put the orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and red blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks) and the middle row (green and orange blocks) are built']. Remaining goals: ['put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the green and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks), the middle row (green and orange blocks), and the top row (the white block) are built']. All goals are completed.\n"+
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
                "Final goal state: ['the red, blue, and green blocks make the bottom row; the yellow and orange blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears on the middle brown block of the stand.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple block appears on the middle brown block of the stand] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['a red block is on the stand'] is unaffected; the task feasibility is affected since the remaining target objects [blue block, green block, yellow block, orange block, pink block] are still available.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['a red block is on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The red and blue blocks are on the stand']. Remaining goals: ['put the green block on the darkest brown block of the stand to complete the bottom row'; 'put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block is placed on the red and blue blocks.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block is placed on the red and blue blocks] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The bottom row (red, blue, and green blocks) is built'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, orange block, pink block] are still available.\n"+
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
                "put the red block on the red and blue blocks into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed on the blue and green blocks.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears on the blue and green blocks] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The yellow block is on top of the built bottom row (red, blue, and green blocks)'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, pink block] are still available.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (red, blue, and green blocks) is built, and the yellow block is on top of the bottom row']. Remaining goals: ['put the orange block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) and the middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks), the middle row (yellow and orange blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
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
                "Final goal state: ['the cyan, pink, and gray blocks make the bottom row; the white and green blocks make the middle row; the orange block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the cyan block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a cyan block is on the stand']. Remaining goals: ['put the pink and gray blocks on the stand to make the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The cyan and pink blocks are on the stand']. Remaining goals: ['put the gray block on the darkest brown block of the stand to complete the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the gray block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen stand appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen stand appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The bottom row (cyan, pink, and gray blocks) is built'] is unaffected; the task feasibility is unaffected since the remaining target objects [white block, green block, orange block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly stand [stand at the top right] as the target stand since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly stand to prevent confusion.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the stand at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (cyan, pink, and gray blocks) is built']. Remaining goals: ['put the white block on the bottom row to make the middle row'; 'put the green block on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the white block on the cyan and pink blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks) is built, and the white block is on top of the bottom row']. Remaining goals: ['put the green block on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the pink and gray blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks) and the middle row (white and green blocks) are built']. Remaining goals: ['put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the orange block on the white and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks), the middle row (white and green blocks), and the top row (the orange block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
        
            anomaly_episode_list=[episode_2,episode_3,episode_4,episode_5]
        elif anomaly_type=="removal":
            episode_1 = (
                "### User:\n" +
                "In the initial state, there are red, green, blue, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the red, green, blue, yellow, orange, and pink blocks'\n"+
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Final goal state: ['The red, green, and blue blocks make the bottom row; the yellow and orange blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A red block is on the stand']. The remaining goals are ['Put the green and blue blocks on the stand to make the bottom row'; 'Put the yellow and orange blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the green block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert.\n" +
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
                "Final goal state: ['The blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the blue block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A blue block is on the stand']. The remaining goals are ['Put the yellow and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the yellow block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
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
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the red block on the blue and yellow blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) and the middle row (red block) are built']. Remaining goals: ['Put the purple block on the middle row to complete it'; 'Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the purple block on the yellow and green blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the pink block on the red and purple blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n" +
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
                "Final goal state: ['The cyan, white, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the cyan block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A cyan block is on the stand']. The remaining goals are ['Put the white and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "put the white block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow block on the table disappears.\n" +
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
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert.\n" +
                "### User:\n" +
                "What is your next plan?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3]
        elif anomaly_type=="displcement":
            episode_1 = (
                "### User:\n"+
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and brown blocks; there is a stand and a trash can. The instruction is 'Please stack the pyramid with the blue, yellow, green, red, purple, and pink blocks'\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and the blue block on the stand is moved to another position on the table.\n"+
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
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The blue and yellow blocks are on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and the green block on the stand is moved to another position on the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the green block back to the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
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
                "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "Progress: ['A blue block is on the stand']. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and yellow blocks are on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and the blue and yellow blocks on the stand are moved to other positions of the table.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the blue and yellow blocks back to the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and green blocks are on the stand']. The remaining goal is ['put the yellow block on the middle brown block of the stand'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your next plan?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2]
        
        
    return anomaly_episode_list    