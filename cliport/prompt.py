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


def get_cot_prompt(task, anomaly_type="pick"):
    please_help=get_help_infomation(task)
   
    if anomaly_type=="None":
        episode_list=get_normal_execution(task=task)[:5]
    else:
        episode_list=get_normal_execution(task=task)[:3]
        episode_list+=get_cot_handling_prompt(task=task,anomaly_type=anomaly_type)
    
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
                    "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Red block -> Red bowl, Purple block -> Purple bowl. The yellow block does not have a corresponding bowl, and the cyan and blue bowls do not have corresponding blocks. The final goal state is ['Green, red, and purple blocks are in their corresponding bowls'].\n"+          
                    "### User:\n"+
                    "What is your plan for the next step?\n" +
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n" +
                    "### User:\n"+
                    'The action succeeded, and no anomaly happened.\n'+
                    "### User:\n"+
                    'Please describe The progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the red and purple blocks in their corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n" +
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe The progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green and red blocks are in their corresponding bowls']. The remaining goal is ['put the purple block in its corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the purple block in the purple bowl.\n" +
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    'Please describe The progress and the remaining goals.\n'+
                    "### Assistant:\n"+
                    "The progress is ['the green, red and purple blocks are in their corresponding bowls']. All goals are completed.\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n" +
                    "### Assistant:\n"+
                    "done.\n"
                    )
        
        example_2 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, and orange bowls; and a trash can.\n" +
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Orange block -> Orange bowl. The green, cyan, and pink blocks do not have corresponding bowls. The final goal state is ['Yellow, blue, and orange blocks are in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n" +
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue and orange blocks in their corresponding bowls'].\n" +
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow, blue, and orange blocks are in their corresponding bowls.']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n") 
        
        example_3 = ("### User:\n"+
                    "In the initial state, there are white, red, pink, and green blocks; there are white, red, pink, yellow, and cyan bowls; and a trash can.\n" +
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"
                    "### Assistant:\n"+
                    "The initial state contains the following pairs of blocks and matching bowls: White block -> White bowl, Red block -> Red bowl, Pink block -> Pink bowl. The green block does not have a corresponding bowl, and the yellow and cyan bowls do not have corresponding blocks. The goal state is ['White, red, and pink blocks are in the corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the red and pink blocks in their corresponding bowls'].\n"+
                    "### User:\n"+"What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the red block in the red bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white and red blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'.]\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the pink block in the pink bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, red, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your plan for the next step? \n"+
                    "### Assistant:\n"+
                    "done.\n")
                    
        example_4 = ("### User:\n"+
                    "In the initial state, there are yellow, blue, orange, green, cyan, and pink blocks; there are yellow, blue, orange, red, and white bowls; and a trash can.\n"+ 
                    #"{please_help}\n"+ 			
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+
                    "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Orange block -> Orange bowl. The green, cyan, and pink blocks do not have corresponding bowls, and the red and white bowls do not have corresponding blocks. The final goal state is ['Yellow, blue, and orange blocks are in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the blue block in the blue bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the yellow, blue, and orange blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_5 = ("### User:\n"+
                    "In the initial state, there are white, green, yellow, orange, blue, and pink blocks; there are white, green, yellow, orange, and purple bowls; and a trash can.\n"+
                    #"{please_help}\n"+
                    "What is the final goal state?\n"+
                    "### Assistant:\n"+"The initial state contains the following pairs of blocks and matching bowls: White block -> White bowl, Green block -> Green bowl, Yellow block -> Yellow bowl, Orange block -> Orange bowl. The blue and pink blocks do not have corresponding bowls, and the bowls with purple color do not have corresponding blocks. The final goal state is ['White, green, yellow, and orange blocks are in their corresponding bowls'].\n"+                   
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the white block in the white bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the green, yellow, and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the green block in the green bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white and green blocks are in their corresponding bowls']. The remaining goal is ['put the yellow and orange blocks in their corresponding bowls'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+"put the yellow block in the yellow bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, green, and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the orange block in its corresponding bowl'].\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "put the orange block in the orange bowl.\n"+
                    "### User:\n"+
                    "The action succeeded, and no anomaly happened.\n"+
                    "### User:\n"+
                    "Please describe The progress and the remaining goals.\n"+
                    "### Assistant:\n"+
                    "The progress is ['the white, green, yellow, and orange blocks are in their corresponding bowls']. All goals are completed.\n"+
                    "### User:\n"+
                    "What is your plan for the next step?\n"+
                    "### Assistant:\n"+
                    "done.\n")
        
        example_6=(
            "### User:\n"+
            "In the initial state, there are white, blue, yellow, green, pink, and red blocks; there are white, blue, yellow, orange, cyan, and purple bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The initial state contains the following pairs of blocks and matching bowls: White block -> White bowl, Blue block -> Blue bowl, Yellow block -> Yellow bowl. The green, pink, and red blocks do not have corresponding bowls, and the orange, cyan, and purple bowls do not have corresponding blocks. The final goal state is ['White, blue, and yellow blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the white block in the white bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the blue and yellow blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white and blue blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the white, blue, and yellow blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_7=(
            "### User:\n"+ 
            "In the initial state, there are red, green, blue, cyan, pink, and orange blocks; there are red, green, blue, cyan, yellow, and purple blocks; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The initial state contains the following pairs of blocks and matching bowls: Red block -> Red bowl, Green block -> Green bowl, Blue block -> Blue bowl, Cyan block -> Cyan bowl. The pink and orange blocks do not have corresponding bowls, and the yellow and purple bowls do not have corresponding blocks. The final goal state is ['Red, green, blue, and cyan blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red block is in its corresponding bowl']. The remaining goal is ['put the green, blue, and cyan blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue and cyan blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red, green, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the cyan block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the cyan block in the cyan bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the red, green, blue, and cyan blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_8=(
            "### User:\n"+
            "In the initial state, there are purple, yellow, green, blue, white, and red blocks; there are purple, yellow, green, blue, orange, and pink bowls; and a trash can.\n"+
            #"{please_help}\n"+ 
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The initial state contains the following pairs of blocks and matching bowls: Purple block -> Purple bowl, Yellow block -> Yellow bowl, Green block -> Green bowl, Blue block -> Blue bowl. The white and red blocks do not have corresponding bowls, and the orange and pink bowls do not have corresponding blocks. The final goal state is ['Purple, yellow, green, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the purple block in the purple bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple block is in its corresponding bowl']. The remaining goal is ['put the yellow, green, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the green and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple, yellow, and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the purple, yellow, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
            
        )
        example_9=(
            "### User:\n"+ 
            "In the initial state, there are orange, red, green, blue, pink, and cyan blocks; there are orange, red, green, blue, purple, and yellow bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The initial state contains the following pairs of blocks and matching bowls: Orange block -> Orange bowl, Red block -> Red bowl, Green block -> Green bowl, Blue block -> Blue bowl. The pink and cyan blocks do not have corresponding bowls, and the purple and yellow bowls do not have corresponding blocks. The final goal state is ['Orange, red, green, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block in the orange bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange block is in its corresponding bowl']. The remaining goal is ['put the red, green, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange and red blocks are in their corresponding bowls']. The remaining goal is ['put the green and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange, red, and green blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the orange, red, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        
        example_10=(
            "### User:\n"+ 
            "In the initial state, there are yellow, green, red, blue, orange, and purple blocks; there are yellow, green, red, blue, pink, and cyan bowls; and a trash can.\n"+
            #"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Green block -> Green bowl, Red block -> Red bowl, Blue block -> Blue bowl. The orange and purple blocks do not have corresponding bowls, and the pink and cyan bowls do not have corresponding blocks. The final goal state is ['Yellow, green, red, and blue blocks are in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the yellow bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the green, red, and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the green bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow and green blocks are in their corresponding bowls']. The remaining goal is ['put the red and blue blocks in their corresponding bowls'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the red bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow, green, and red blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the blue bowl.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe The progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['the yellow, green, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
            
        )
        episode_list=[example_1,example_2,example_3,example_4,example_5,example_6,example_7,example_8,example_9,example_10]
    
    elif task=="packing-boxes":
        episode_1=(
            "### User:\n"+
            "In the initial state, there are red, blue, green, yellow, orange, and purple blocks; there is a brown box and a trash can.\n"+
            ##"{please_help}\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Red block, blue block, red block, green block, blue block, and yellow block are in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A red block is in the brown box']. The remaining goal is ['Put blue block, red block, green block, blue block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A red block and a blue block are in the brown box']. The remaining goal is ['Put red block, green block, blue block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, and red block are in the brown box']. The remaining goal is ['Put green block, blue block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, red block, and green block are in the brown box']. The remaining goal is ['Put blue block and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, red block, green block, and blue block are in the brown box']. The remaining goal is ['Put the yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, red block, green block, blue block, and yellow block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n")
        
        episode_2=("### User:\n"+
            "In the initial state, there are orange, pink, orange, cyan, orange, and pink blocks; there is a brown box and a trash can.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Orange block, pink block, orange block, cyan block, orange block, and pink block are in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['An orange block is in the brown box']. The remaining goal is ['Put pink block, orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['An orange block and a pink block are in the brown box']. The remaining goal is ['Put orange block, cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Orange block, pink block, and orange block are in the brown box']. The remaining goal is ['Put cyan block, orange block, and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the cyan block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Orange block, pink block, orange block, and cyan block are in the brown box']. The remaining goal is ['Put orange block and pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Orange block, pink block, orange block, cyan block, and orange block are in the brown box']. The remaining goal is ['Put the pink block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the pink block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Orange block, pink block, orange block, cyan block, orange block, and pink block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n")

        
        episode_3=("### User:\n"+
            "In the initial state, there are blue, gray, blue, green, white, and yellow blocks; there is a brown box and a trash can.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Blue block, gray block, blue block, brown block, white block, and yellow block are in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A blue block is in the brown box']. The remaining goal is ['Put gray block, blue block, brown block, white block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the gray block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A blue block and a gray block are in the brown box']. The remaining goal is ['Put blue block, brown block, white block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Blue block, gray block, and blue block are in the brown box']. The remaining goal is ['Put green block, white block, and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Blue block, gray block, blue block, and green block are in the brown box']. The remaining goal is ['Put white block and yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put a white block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Blue block, gray block, blue block, brown block, and a white block are in the brown box']. The remaining goal is ['Put the yellow block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Blue block, gray block, blue block, brown block, white block, and yellow block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n")

        episode_4=("### User:\n"+
            "In the initial state, there are red, blue, green, yellow, orange, and purple blocks; there is a brown box and a trash can.\n"+
            ##"{please_help}\n"+            
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "The final goal state is ['Red block, blue block, green block, yellow block, orange block, and purple block are in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A red block is in the brown box']. The remaining goal is ['Put blue block, green block, yellow block, orange block, and purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['A red block and a blue block are in the brown box']. The remaining goal is ['Put green block, yellow block, orange block, and purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, and green block are in the brown box']. The remaining goal is ['Put yellow block, orange block, and purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, green block, and yellow block are in the brown box']. The remaining goal is ['Put orange block and purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, green block, yellow block, and orange block are in the brown box']. The remaining goal is ['Put purple block in the brown box'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the purple block in the brown box.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "The progress is ['Red block, blue block, green block, yellow block, orange block, and purple block are in the brown box']. All goals are completed.\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )

        episode_list=[episode_1,episode_2,episode_3,episode_4]
    
    elif "pyramid" in task:
        episode_1=(
            "### User:\n"+
            "In the initial state, there are gray, red, blue, brown, white, pink, and green blocks; there is a stand and a trash can.\n"+
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Final goal state: ['the gray, red, and blue blocks make the bottom row; the brown and white blocks make the middle row; the pink block makes the top row'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"
            "### Assistant:\n"+
            "Progress: [a gray block is on the stand]. Remaining goals: ['put the red and blue blocks on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"
            "### Assistant:\n"+
            "Progress: [The gray and red blocks are on the stand]. Remaining goals: ['put the blue block on the stand to make the bottom row'; 'put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, red, and blue blocks) is built]. Remaining goals: ['put the brown and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the brown block on the gray and red blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, red, and blue blocks) is built, and the brown block is on top of the bottom row]. Remaining goals: ['put the white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the white block on the red and blue blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, red, and blue blocks) and the middle row (brown and white blocks) are built]. Remaining goals: ['put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the pink block on the brown and white blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, red, and blue blocks), the middle row (brown and white blocks), and the top row (the pink block) are built]. All goals are completed\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n")
		
        episode_2 = (
            "### User:\n" +
            "In the initial state, there are yellow, blue, red, orange, green, brown, pink, and gray blocks; there is a stand and a trash can.\n" +
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Final goal state: ['the yellow, blue, and red blocks make the bottom row; the orange and green blocks make in the middle row; the brown block makes the top row'].\n" +
            "### User:\n" +
            "What is your plan for the next step?\n" +
            "### Assistant:\n" +
            "put the yellow block on the lightest brown block of the stand.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a yellow block is on the stand]. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your plan for the next step?\n" +
            "### Assistant:\n" +
            "put the blue block on the middle brown block of the stand.\n" +
			"### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The yellow and blue blocks are on the stand]. Remaining goals: ['put the red block on the stand to make the bottom row'; 'put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (yellow, blue, and red blocks) is built]. Remaining goals: ['put the orange and green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n" +
            "What is your plan for the next step?\n" +
            "### Assistant:\n" +
            "put the orange block on the yellow and blue blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (yellow, blue, and red blocks) is built, the orange block is on top of the bottom row]. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the green block on the blue and red blocks.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (yellow, blue, and red blocks) and the middle row (orange and green blocks) are built]. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the brown block on the orange and green blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
			"### User:\n"+
			"Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (yellow, blue, and red blocks), the middle row (orange and green blocks), and the top row (the brown block) are built]. All goals are completed\n"+
			"### User:\n"+
            "What is your plan for the next step?\n" +
            "### Assistant:\n" +
            "done.\n")
        
        episode_3=(
            "### User:\n" +
            "In the initial state, there are orange, purple, white, green, yellow, brown, and pink blocks; there is a stand and a trash can.\n" +
            "What is the final goal state?\n" +
            "### Assistant:\n" +
            "Final goal state: ['the orange, purple, and white blocks make the bottom row; the green and yellow blocks make the middle row; the brown block makes the top row'].\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the orange block on the lightest brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [an orange block is on the stand]. Remaining goals: ['put the purple and white blocks on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the purple block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The orange and purple blocks are on the stand]. Remaining goals: ['put the white block on the stand to make the bottom row'; 'put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the white block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (orange, purple, and white blocks) is built]. Remaining goals: ['put the green and yellow blocks on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the green block on the orange and purple blocks.\n" +
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (orange, purple, and white blocks) is built, and the green block is on top of the bottom row]. Remaining goals: ['put the yellow block on top of the bottom row to make the middle row'; 'put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block on the purple and white blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (orange, purple, and white blocks) and the middle row (green and yellow blocks) are built]. Remaining goals: ['put the brown block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the brown block on the green and yellow blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (orange, purple, and white blocks), the middle row (green and yellow blocks), and the top row (the brown block) are built]. All goals are completed\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "done.\n")
        
        episode_4=(
            "### User:\n" +
            "In the initial state, there are gray, pink, yellow, red, green, blue, and purple blocks; there is a stand and a trash can.\n" +
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Final goal state: ['the gray, pink, and yellow blocks make bottom row; the red and green blocks make the middle row; the blue block makes the top row'].\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the gray block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a gray block is on the stand]. Remaining goals: ['put the pink and yellow blocks on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the pink block on the middle brown block of the stand.\n" +
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The gray and pink blocks are on the stand]. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the yellow block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: [The bottom row (gray, pink, and yellow blocks) is built]. Remaining goals: ['put the red and green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n" +
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block on the gray and pink blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n" +
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n" +
            "### Assistant:\n"+
            "Progress: [The bottom row (gray, pink, and yellow blocks) is built, and red block is on top of the bottom row]. Remaining goals: ['put the green blocks on top of the bottom row to make the middle row'; 'put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the green block on the pink and yellow blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (gray, pink, and yellow blocks) and the middle row (red and green blocks) are built]. Remaining goals: ['put the blue block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the blue block on the red and green blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n" +
            "Progress: [The bottom (gray, pink, and yellow blocks), the middle row (red and green blocks), and the top row (the blue block) are built]. All goals are completed\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )

        episode_5=(
            "### User:\n" +
            "In the initial state, there are blue, yellow, green, red, white, pink, and orange blocks; there is a stand and a trash can.\n" +
            "What is the final goal state?\n"+
            "### Assistant:\n"+
            "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and white blocks make the middle row; the pink block makes the top row'].\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the blue block on the lightest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [a blue block is on the stand]. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the yellow block on the middle brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The blue and yellow blocks are on the stand]. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and white blocks on  top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the green block on the darkest brown block of the stand.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (blue, yellow, and green blocks) is built]. Remaining goals: ['put the red and white blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n" +
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the red block on the blue and yellow blocks.\n"+
            "### User:\n" +
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row]. Remaining goals: ['put the white block on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "put the white block on the yellow and green blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (blue, yellow, and green blocks) and the middle row (red and white blocks) are built]. Remaining goals: ['put the pink block on top of the middle row to make the top row']\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n" +
            "put the pink block on the red and white blocks.\n"+
            "### User:\n"+
            "The action succeeded, and no anomaly happened.\n"+
            "### User:\n"+
            "Please describe the achieved progress and the remaining goals.\n"+
            "### Assistant:\n"+
            "Progress: [The bottom (blue, yellow, and green blocks), the middle row (red and white blocks), and the top row (the pink block) are built]. All goals are completed\n"+
            "### User:\n"+
            "What is your plan for the next step?\n"+
            "### Assistant:\n"+
            "done.\n"
        )
        episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
                "### Assistant:\n"+
                "put the red block in the red bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe The progress and the remaining goals.\n'+
                "### Assistant:\n"+
                "The progress is ['the blue, green, and red blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowls'].\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n" +
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                'Please describe The progress and the remaining goals.\n'+
                "### Assistant:\n"+
                "The achieves progress is ['the blue, green, red and yellow blocks are in their corresponding bowls']. All goals are completed.\n" +
                "### User:\n"+
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "What is your plan for the next step?\n" +
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
                "The initial state contains the following pairs of blocks and matching bowls: Cyan block -> Cyan bowl, Yellow block -> Yellow bowl, Orange block -> Orange bowl, Blue block -> Blue bowl. The red and purple blocks do not have corresponding bowls, and the brown and white bowls do not have their corresponding blocks. The final goal state is ['Cyan, yellow, orange, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan block is in its corresponding bowl']. The remaining goal is ['put the yellow, orange, and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the orange and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the cyan and yellow blocks in their corresponding bowls are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the cyan and yellow blocks in their corresponding bowls are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the cyan and yellow blocks are not in their corresponding bowls; the current progress is ['the orange block is in its corresponding bowl']; the remaining target objects [cyan block, cyan bowl, yellow block, yellow bowl, blue block, blue bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the cyan and yellow blocks back to their corresponding bowls.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the cyan and orange blocks are in their corresponding bowls']. To address this anomaly, the remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the cyan, yellow, and orange blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the cyan, yellow, orange, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_2=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, pink, gray, and green blocks; there are yellow, blue, red, pink, and purple bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Red block -> Red bowl, Pink block -> Pink bowl. The gray and green blocks do not have their corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Yellow, blue, red, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue, red, and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow and blue blocks are in their corresponding bowls']. The remaining goal is ['put the red and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the yellow and blue blocks in their corresponding bowls are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the yellow and blue blocks in their corresponding bowls are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the yellow and blue blocks are not in their corresponding bowls; the current progress is ['the red block is in its corresponding bowl']; the remaining target objects [yellow block, yellow bowl, blue block, blue bowl, pink block, pink bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the yellow and blue blocks back to their corresponding bowls.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the red and yellow blocks are in their corresponding bowls']. To address this anomaly, the remaining goal is ['put the blue block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red, yellow, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, yellow, blue, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
                )
            episode_3=(
                "### User:\n"+
                "In the initial state, there are red, green, blue, yellow, pink, and white blocks; there are red, green, blue, yellow, and orange bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Red block -> Red bowl, Green block -> Green bowl, Blue block -> Blue bowl, Yellow block -> Yellow bowl. The pink and white blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. The final goal state is ['Red, green, blue, and yellow blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red block is in its corresponding bowl']. The remaining goal is ['put the green, blue, and yellow blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the red block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the red block in its corresponding bowl is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the red block is not in its corresponding bowl; the current progress is ['the green block is in its corresponding bowl']; the remaining target objects [red block, red bowl, blue block, blue bowl, yellow block, yellow bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the red block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red and green blocks are in their corresponding bowls']; the remaining goal is ['put the blue and yellow blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, green, and blue blocks are in their corresponding bowls']. The remaining goal is ['put the yellow block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, green, blue, and yellow blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_4=(
                "### User:\n"+
                "In the initial state, there are green, blue, pink, orange, red, and purple blocks; there are green, blue, pink, yellow, and white bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Blue block -> Blue bowl, Pink block -> Pink bowl. The orange, red, and purple blocks do not have corresponding bowls, and the yellow and white bowls do not have corresponding blocks. The final goal state is ['Green, blue, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the blue and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the green block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the green block in its corresponding bowl is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the green block is not in its corresponding bowl; the current progress is ['the blue block is in its corresponding bowl']; the remaining target objects [green block, green bowl, pink block, pink bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the green block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The achieved progress is ['the green and blue blocks are in their corresponding bowls']; the remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, blue, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            episode_5=(
                "### User:\n"+
                "In the initial state, there are brown, blue, green, red, yellow, and pink blocks; there are brown, blue, green, and purple bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Brown block -> Brown bowl, Blue block -> Blue bowl, Green block -> Green bowl. The red, yellow, and pink blocks do not have corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Brown, blue, and green blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the brown block in the brown bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the brown block is in its corresponding bowl']. The remaining goal is ['put the blue and green blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the brown and blue blocks are in their corresponding bowls']. The remaining goal is ['put the green block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and the brown block in its corresponding bowl is moved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the brown block in its corresponding bowl is moved to another position on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the brown block is not in its corresponding bowl; the current progress is ['the blue and green blocks are in their corresponding bowls']; the remaining target objects [brown block, brown bowl] are available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "put the brown block back to its corresponding bowl.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the brown block in the brown bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The achieved progress is ['the brown, blue, and green blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4,episode_5]
        
        elif anomaly_type=="addition":
            ## add two episodes for "pick", "place", and "container", respectively.
            episode_1=(
                        "### User:\n"+
                        "In the initial state, there are blue, pink, red, purple, and white blocks; there are blue, pink, red, purple, yellow and cyan bowls; and a trash can.\n"+
                        #"{please_help}\n"+ 
                        "What is the final goal state?\n"+
                        "### Assistant:\n"+
                        "The initial state contains the following pairs of blocks and matching bowls: Blue block -> Blue bowl, Pink block -> Pink bowl, Red block -> Red bowl, Purple block -> Purple bowl. The white block does not have a corresponding bowl, and the yellow and cyan bowls do not have corresponding blocks. The final goal state is ['Blue, pink, red, and purple blocks are in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the blue block in the blue bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the blue block is in its corresponding bowl']. The remaining goal is ['put the pink, red, and purple blocks in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the pink block in the pink bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen orange block appears at the bottom right.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly [a never-seen orange block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                        "### Assistant:\n"+
                        "The progress ['The blue and pink blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, purple block, purple bowl] are still available.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly on future actions.\n"+
                        "### Assistant:\n"+
                        "The robot will not be affected since the anomaly block [orange block at the bottom right] is not a target object and has a different color from any target blocks.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "No action needed\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the red block in the red bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen purple block appears at the top right.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly [a never-seen purple block appears at the top right] on the task regarding progress and feasibility.\n"+
                        "### Assistant:\n"+
                        "The progress ['The blue, pink, and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [purple block, purple bowl] are still available.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly on future actions.\n"+
                        "### Assistant:\n"+
                        "The robot may mistake the anomaly block [purple block at the top right] for the target purple block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "Remove the anomaly block to prevent confusion.\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the purple block at the top right into the trash can.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The anomaly has been addressed. The progress is ['the blue, pink, and red blocks are in their corresponding bowls']. The remaining goal is ['put the purple block in its corresponding bowl'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the purple block in the purple bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the blue, pink, red, and purple blocks are in their corresponding bowls']. All goals are completed.\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "done.\n")
            
            episode_2=(
                        "### User:\n"+
                        "In the initial state, there are green, yellow, red, blue, white, and cyan blocks; there are green, yellow, red, blue, and orange bowls; and a trash can.\n" +
                        #"{please_help}\n"+ 
                        "What is the final goal state?\n" +
                        "### Assistant:\n" +
                        "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl. The white and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. The final goal state is ['Green, yellow, red, and blue blocks are in their corresponding bowls'].\n" +
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n" +
                        "put the green block in the green bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and a never-seen white block appears at the bottom left.\n" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly [a never-seen white block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n" +
                        "The progress ['The green block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [yellow block, yellow bowl, red block, red bowl, blue block, blue bowl] are still available.\n" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n" +
                        "The robot will not be affected since the anomaly block [white block at the bottom left] is not a target object and has a different color from any target blocks.\n" +
                        "### User:\n" +
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n" +
                        "No action needed\n" +
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n" +
                        "put the yellow block in the yellow bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and a never-seen blue block appears at the top right" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly [a never-seen blue block appears at the top right] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n" +
                        "The progress ['The green, yellow blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, blue block, blue bowl] are still available.\n" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n" +
                        "The robot may mistake the anomaly block [blue block at the top right] for the target blue block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "Remove the anomaly block to prevent confusion.\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the blue block at the top right into the trash can.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The anomaly has been addressed. The progress is ['the green and yellow blocks are in their corresponding bowls']. The remaining goal is ['put the red and blue block in its corresponding bowl'].\n"+
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n" +
                        "put the red block in the red bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and a never-seen cyan block appears at the bottom left.\n" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly [a never-seen cyan block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n" +
                        "The progress ['The green, yellow, and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl] are still available.\n" +
                        "### User:\n" +
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n" +
                        "The robot will not be affected since the anomaly block [cyan block at the top right] is not a target object and has a different color from any target blocks.\n" +
                        "### User:\n" +
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n" +
                        "No action needed\n" +
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n" +
                        "put the blue block in the blue bowl.\n" +
                        "### User:\n" +
                        "The action succeeded, and no anomaly happened.\n" +
                        "### User:\n" +
                        "Please describe The progress and the remaining goals.\n" +
                        "### Assistant:\n" +
                        "The progress is ['the green, yellow, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n" +
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n" +
                        "done.\n"
            )
            
            episode_3=(
                        "### User:\n"+
                        "In the initial state, there are white, red, blue, pink, green, and cyan blocks; there are white, red, blue, pink, and yellow bowls; and a trash can.\n" +
                        #"{please_help}\n"+ 
                        "What is the final goal state?\n" +
                        "### Assistant:\n"
                        "The initial state contains the following pairs of blocks and matching bowls: White block -> White bowl, Red block -> Red bowl, Blue block -> Blue bowl, Pink block -> Pink bowl. The green and cyan blocks do not have corresponding bowls, and the yellow bowl does not have a corresponding block. The final goal state is ['White, red, blue, and pink blocks are in their corresponding bowls'].\n" +
                        "### User:\n"
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "put the white block in the white bowl.\n" +
                        "### User:\n"
                        "The action succeeded, and no anomaly happened.\n" +
                        "### User:\n"
                        "Please describe The progress and the remaining goals.\n" +
                        "### Assistant:\n"
                        "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the red, blue, and pink blocks in their corresponding bowls'].\n" +
                        "### User:\n"
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "put the red block in the red bowl.\n" +
                        "### User:\n"
                        "The action succeeded, and a never-seen blue block appears at the top right.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly [a never-seen blue block appears at the top right] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n"
                        "The progress ['The white and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl, pink block, pink bowl] are still available.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n"
                        "The robot may mistake the anomaly block [blue block at the top right] for the target blue block since they have the same color. To avoid confusion, the anomaly block should be removed.\n" +
                        "### User:\n"
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n"
                        "Remove the anomaly block to prevent confusion.\n" +
                        "### User:\n"
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "put the blue block at the top right into the trash can.\n" +
                        "### User:\n"
                        "The action succeeded, and no anomaly happened.\n" +
                        "### User:\n"
                        "Please describe The progress and the remaining goals.\n" +
                        "### Assistant:\n"
                        "The anomaly has been addressed. The progress is ['the white and red blocks are in their corresponding bowls']. The remaining goal is ['put the blue and pink blocks in their corresponding bowls'].\n" +
                        "### User:\n"
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "put the blue block in the blue bowl.\n" +
                        "### User:\n"
                        "The action succeeded, and a never-seen green block appears at the top left.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly [a never-seen green block appears at the top left] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n"
                        "The progress ['The white, red, and blue blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, pink bowl] are still available.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n" +
                        "The robot will not be affected since the anomaly block [green block at the top left] is not a target object and has a different color from any target blocks.\n" +
                        "### User:\n" +
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n" +
                        "No action needed\n" +
                        "### User:\n" +
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "put the pink block in the pink bowl.\n" +
                        "### User:\n"
                        "The action succeeded, and a never-seen cyan block appears at the bottom right.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly [a never-seen cyan block appears at the bottom right] on the task regarding progress and feasibility.\n" +
                        "### Assistant:\n"
                        "The progress ['The white, red, blue, and pink blocks are in their corresponding bowls'] is unaffected; all goals are completed.\n" +
                        "### User:\n"
                        "Analyze the effect of the anomaly on future actions.\n" +
                        "### Assistant:\n" +
                        "The robot will not be affected since the anomaly block [green block at the top left] is not a target object and has a different color from any target blocks.\n" +
                        "### User:\n" +
                        "How to handle this anomaly?\n" +
                        "### Assistant:\n" +
                        "No action needed\n" +
                        "### User:\n"
                        "What is your plan for the next step?\n" +
                        "### Assistant:\n"
                        "done.\n"
            )
            
            
            episode_4=(
                        "### User:\n"+
                        "In the initial state, there are green, gray, orange, pink, red, and blue blocks; there are green, gray, orange, pink, and purple bowls; and a trash can.\n"+
                        #"{please_help}\n"+
                        "What is the final goal state?\n"+
                        "### Assistant:\n"+
                        "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Gray block -> Gray bowl, Orange block -> Orange bowl, Pink block -> Pink bowl. The red and blue blocks do not have corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Green, gray, orange, and pink blocks are in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the green block in the green bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen pink block appears at the bottom right.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly [a never-seen pink block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                        "### Assistant:\n"+
                        "The progress ['The green block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [gray block, gray bowl, orange block, orange bowl, pink block, pink bowl] are still available.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly on future actions.\n"+
                        "### Assistant:\n"+
                        "The robot may mistake the anomaly block [pink block at the bottom right] for the target pink block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "Remove the anomaly block to prevent confusion.\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the pink block at the bottom right into the trash can.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The anomaly has been addressed. The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the gray, orange, and pink blocks in their corresponding bowl'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the gray block in the gray bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the green and gray blocks are in their corresponding bowls']. The remaining goal is ['put the orange and pink blocks in their corresponding bowls'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the orange block in the orange bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and no anomaly happened.\n"+
                        "### User:\n"+
                        "Please describe The progress and the remaining goals.\n"+
                        "### Assistant:\n"+
                        "The progress is ['the green, gray, and orange blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "put the pink block in the pink bowl.\n"+
                        "### User:\n"+
                        "The action succeeded, and a never-seen cyan block appears at the top left.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly [a never-seen cyan block appears at the top left] on the task regarding progress and feasibility.\n"+
                        "### Assistant:\n"+
                        "The progress ['The green, gray, orange, and pink blocks are in their corresponding bowls'] is unaffected; all goals are completed.\n"+
                        "### User:\n"+
                        "Analyze the effect of the anomaly on future actions.\n"+
                        "### Assistant:\n"+
                        "The robot will not be affected since the anomaly block [cyan block at the top left] is not a target object and has a different color from any target blocks.\n"+
                        "### User:\n"+
                        "How to handle this anomaly?\n"+
                        "### Assistant:\n"+
                        "No action needed\n"+
                        "### User:\n"+
                        "What is your plan for the next step?\n"+
                        "### Assistant:\n"+
                        "done.\n"  
            )
            
            episode_5=(
                "### User:\n"+
                "In the initial state, there are green, yellow, cyan, purple, and pink blocks; there are green, yellow, cyan, purple, and blue bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Yellow block -> Yellow bowl, Cyan block -> Cyan bowl, Purple block -> Purple bowl. The pink block does not have corresponding bowls, and the blue bowl does not have corresponding blocks. The final goal state is ['Green, yellow, cyan, and purple blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the yellow, cyan, and purple blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green and yellow blocks are in their corresponding bowls'] is unaffected; the remaining target objects [cyan block, cyan bowl, purple block, purple bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [pink block at the bottom right] is not a target object and has a different color from any target blocks.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple block appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green, yellow, and cyan blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [purple block, purple bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [purple block at the bottom left] for the target purple block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block at the bottom left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the green, yellow, and cyan blocks are in their corresponding bowls']. The remaining goal is ['put the purple block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block in the purple bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, yellow, cyan, and purple blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n")
            ## address the perturbation when the added block in the non-target bowls
            episode_6=(
                "### User:\n"+
                "In the initial state, there are orange, white, cyan, green, and yellow blocks; there are bowls with orange, white, cyan, and gray bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Orange block -> Orange bowl, White block -> White bowl, Cyan block -> Cyan bowl. The green and yellow blocks do not have corresponding bowls, and the gray bowl does not have a corresponding block. The final goal state is ['Orange, cyan, and white blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block is placed into the white bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block is placed in the white bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The orange block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [cyan block, cyan bowl, white block, white bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [red block in the white bowl] takes the free space of the target white bowl, and the robot may not find a space to put the target white block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the white bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the orange block is in its corresponding bowl']. The remaining goal is ['put the white and cyan blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block in the white bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed into the gray bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block is placed in the gray bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The orange and white blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [cyan block, cyan bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [pink block in the gray bowl] is not placed into any target bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the orange, white, and cyan blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_7=(
                "### User:\n"+
                "In the initial state, there are yellow, red, blue, green, and orange blocks; there are yellow, red, blue, purple, and cyan bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Red block -> Red bowl, Blue block -> Blue bowl. The green and orange blocks do not have corresponding bowls, and the purple and cyan bowls do not have corresponding blocks. The final goal state is ['Yellow, red, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen cyan block is placed into the purple bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen cyan block is placed in the purple bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The yellow block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [cyan block in the purple bowl] is not placed into any target bowl.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen green block appears in the blue bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen green block appears in the blue bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The yellow and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [green block in the blue bowl] takes the free space of the blue bowl, and the robot may not find a space to put the target blue block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the blue bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the yellow and red blocks are in their corresponding bowls']. The remaining goal is ['put the blue block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow, red, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_8=(
                "### User:\n"+
                "In the initial state, there are pink, blue, gray, green, and red blocks; there are pink, blue, gray, yellow, and cyan bowls; and a trash can.\n"+
                #"{please_help}\n"+     
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Pink block -> Pink bowl, Blue block -> Blue bowl, Gray block -> Gray bowl. The green and red blocks do not have corresponding bowls, and the yellow and cyan bowls do not have corresponding blocks. The final goal state is ['Pink, blue, and gray blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the pink block is in its corresponding bowl']. The remaining goal is ['put the blue and gray blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block appears in the gray bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block appears in the gray bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The pink and blue blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [gray block, gray bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [red block in the gray bowl] takes the free space of the gray bowl, and the robot may not find a space to put the target gray block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the gray bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the pink and blue blocks are in their corresponding bowls']. The remaining goal is ['put the gray block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the pink, blue, and gray blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_9=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, pink, and yellow blocks; there are bowls with red, blue, green, and purple bowls; and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Red block -> Red bowl, Blue block -> Blue bowl, Green block -> Green bowl. The pink and yellow blocks do not have corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Red, blue, and green blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block is placed into the blue bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block is placed in the blue bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The red block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl, green block, green bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [yellow block in the blue bowl] takes the free space of the target blue bowl, and the robot may not find a space to put the target blue block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the blue bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red block is in its corresponding bowl']. The remaining goal is ['put the blue and green blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block is placed into the green bowl.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block is placed in the green bowl] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The red and blue blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, green bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [pink block in the green bowl] takes the free space of the target green bowl, and the robot may not find a space to put the target green block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the green bowl into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the red and blue blocks are in their corresponding bowls']. The remaining goal is ['put the green block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the red, blue, and green blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            ## address the perturbation when the addtion is the bowl
            episode_10=(
                "### User:\n"+
                "In the initial state, there are green, pink, gray, red, blue, and cyan blocks; there are green, pink, gray, and orange bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Pink block -> Pink bowl, Gray block -> Gray bowl. The red, blue, and cyan blocks do not have corresponding bowls, and the orange bowl does not have a corresponding block. The final goal state is ['Green, pink, and gray blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray bowl appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray bowl appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green block is in its corresponding bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, pink bowl, gray block, gray bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [gray bowl at the bottom right] for the target gray bowl since they have the same color. To avoid confusion, the anomaly bowl should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray bowl at the bottom right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the pink and gray blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen blue bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen blue bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green and pink blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [gray block, gray bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [blue bowl at the bottom left] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, pink, and gray blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_11=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, pink, gray, and green blocks; there are yellow, blue, red, pink, and purple bowls; and a trash can.\n"+
                #"{please_help}\n"+         
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Yellow block -> Yellow bowl, Blue block -> Blue bowl, Red block -> Red bowl, Pink block -> Pink bowl. The gray and green blocks do not have their corresponding bowls, and the purple bowl does not have a corresponding block. The final goal state is ['Yellow, blue, red, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the yellow bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow block is in its corresponding bowl']. The remaining goal is ['put the blue, red, and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen green bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen green bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The yellow and blue blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, red bowl, pink block, pink bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [green bowl at the bottom left] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
				"### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray bowl appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray bowl appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The yellow, blue, and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, pink bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [gray bowl at the bottom right] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the yellow, blue, red, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
        
            episode_12=(
                "### User:\n"+
                "In the initial state, there are green, gray, orange, pink, red, blue, and cyan blocks; there are green, gray, orange, pink, and yellow bowls; and a trash can.\n"+
                #"{please_help}\n"+      
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Green block -> Green bowl, Gray block -> Gray bowl, Orange block -> Orange bowl, Pink block -> Pink bowl. The red, blue, and cyan blocks do not have corresponding bowls, and the yellow bowl does not have a corresponding block. The final goal state is ['Green, gray, orange, and pink blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray bowl appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray bowl appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green block is in the green bowl'] is unaffected; the task feasibility is unaffected since the remaining target objects [gray block, gray bowl, orange block, orange bowl, pink block, pink bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [gray bowl at the top right] for the target gray bowl since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray bowl at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the green block is in its corresponding bowl']. The remaining goal is ['put the gray, orange, and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the gray bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The green and gray blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, orange bowl, pink block, pink bowl] are still available.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [pink bowl at the bottom left] for the target pink bowl since they have the same color. To avoid confusion, the anomaly bowl should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink bowl at the bottom left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['The green and gray blocks are in their corresponding bowls']. The remaining goal is ['put the orange and pink blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, gray, and orange blocks are in their corresponding bowls']. The remaining goal is ['put the pink block in its corresponding bowl'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the pink bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the green, gray, orange, and pink blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_13=(
                "### User:\n"+
                "In the initial state, there are white, red, green, blue, yellow, and purple blocks; there are white, red, green, blue, and pink bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: White block -> White bowl, Red block -> Red bowl, Green block -> Green bowl, Blue block -> Blue bowl. The yellow and purple blocks do not have corresponding bowls, and the pink bowl does not have a corresponding block. The final goal state is ['White, red, green, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block in the white bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the white block is in its corresponding bowl']. The remaining goal is ['put the red, green, and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the red bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow bowl appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow bowl appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The white and red blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, green bowl, blue block, blue bowl] are still available.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [yellow bowl at the top right] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen purple bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The white, red, and green blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [purple bowl at the bottom left] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the white, red, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            
            episode_14=(
                "### User:\n"+
                "In the initial state, there are orange, cyan, green, blue, pink, and red blocks; there are orange, cyan, green, and blue bowls; and a trash can.\n"+
                #"{please_help}\n"+ 
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The initial state contains the following pairs of blocks and matching bowls: Orange block -> Orange bowl, Cyan block -> Cyan bowl, Green block -> Green bowl, Blue block -> Blue bowl. The pink and red blocks do not have corresponding bowls. The final goal state is ['Orange, cyan, green, and blue blocks are in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the orange bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the orange block is in its corresponding bowl']. The remaining goal is ['put the cyan, green, and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the cyan bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen blue bowl appears at the bottom left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen blue bowl appears at the bottom left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The orange and cyan blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, green bowl, blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly bowl [blue bowl at the bottom left] for the target blue bowl since they have the same color. To avoid confusion, the anomaly bowl should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly bowl to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue bowl at the bottom left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['the orange and cyan blocks are in their corresponding bowls']. The remaining goal is ['put the green and blue blocks in their corresponding bowls'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the green bowl.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red bowl appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red bowl appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The orange, cyan, and green blocks are in their corresponding bowls'] is unaffected; the task feasibility is unaffected since the remaining target objects [blue block, blue bowl] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly bowl [red bowl at the top right] is not a target object and has a different color from any target bowls.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the blue bowl.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe The progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['the orange, cyan, green, and blue blocks are in their corresponding bowls']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )            
            
            anomaly_episode_list=[episode_6,episode_7,episode_8,episode_9]
    elif "box" in task:
        if anomaly_type=="addition":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, and orange blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Red block, blue block, green block, yellow block, and orange block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A red block is in the brown box']. The remaining goal is ['Put blue block, green block, yellow block, and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears at the top left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears at the top left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A red block and a blue block are in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, orange block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [yellow block appears at the top left] for the target yellow block since they have the same color. To avoid confusion, the anomaly block should be removed.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block at the top left into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['A red block and a blue block are in the brown box']. The remaining goal is ['Put the green block, yellow block, orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Red block, blue block, and green block are in the brown box']. The remaining goal is ['Put yellow block and orange block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the top right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen pink block appears at the top right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['Red block, blue block, green block, and yellow block are in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [pink block at the top right] has a different color from any target blocks.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Red block, blue block, green block, yellow block, and orange block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n")

            episode_2=(
                "### User:\n"+
                "In the initial state, there are cyan, gray, white, pink, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, gray block, white block, pink block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A cyan block is in the brown box']. The remaining goal is ['Put gray block, white block, pink block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A cyan block and a gray block are in the brown box']. The remaining goal is ['Put white block, pink block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears in the brown box.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears in the brown box] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['Cyan block, gray block, and white block are in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [pink block, green block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [yellow block in the brown box] takes the free space of the brown box, and the robot may not find a space to put the target block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The remaining goal is ['Put pink and green blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Cyan block, gray block, white block, and pink block are in the brown box']. The remaining goal is ['Put the green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Cyan block, gray block, white block, pink block, and green block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n")
            
            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, purple, cyan, and white blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Orange block, purple block, cyan block, and white block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['An orange block is in the brown box']. The remaining goal is ['Put purple block, cyan block, and white block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen yellow block appears in the brown box.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen yellow block appears in the brown box] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['Orange block and purple block are in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [cyan block, white block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The anomaly block [yellow block in the brown box] takes the free space of the brown box, and the robot may not find a space to put the target block.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The remaining goal is ['Put cyan and white blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Orange block, purple block, and cyan block are in the brown box']. The remaining goal is ['Put the white block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Orange block, purple block, cyan block, and white block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_4=(
                "### User:\n"+
                "In the initial state, there are pink, blue, gray, cyan, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Pink block, blue block, gray block, cyan block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block is in the brown box']. The remaining goal is ['Put blue block, gray block, cyan block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block and a blue block are in the brown box']. The remaining goal is ['Put gray block, cyan block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen brown box appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen brown box appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['Pink block, blue block, and gray block are in the brown box'] is unaffected; the task feasibility is unaffected since the remaining target objects [cyan block, green block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly box [brown box at the bottom right] as the target brown box since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly brown box to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the the brown box at the bottom right into trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The remaining goal is ['Put cyan and green blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Pink block, blue block, gray block, and cyan block are in the brown box']. The remaining goal is ['Put the green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Pink block, blue block, gray block, cyan block, and green block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n")
            anomaly_episode_list=[episode_1,episode_2,episode_3,episode_4]
    
        elif anomaly_type=="displacement":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are yellow, red, orange, blue, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Yellow block, red block, orange block, blue block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A yellow block is in the brown box']. The remaining goal is ['Put red block, orange block, blue block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A yellow block and a red block are in the brown box']. The remaining goal is ['Put orange block, blue block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the yellow and red blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the yellow and red blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the yellow and red blocks are not in the brown box; the current progress is ['The orange block is in the brown box']. The task feasibility is unaffected since the remaining target objects [yellow block, red block, blue block, green block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the yellow and red blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A yellow block and an orange block are in the brown box']. The remaining goal is ['Put the red block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['Yellow block, red block, and orange block are in the brown box']. The remaining goal is ['Put blue and green blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Yellow block, red block, orange block, and blue block are in the brown box']. The remaining goal is ['Put the green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Yellow block, red block, orange block, blue block, and green block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
                )
            episode_2=(
                "### User:\n"+
                "In the initial state, there are pink, blue, gray, cyan, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Pink block, blue block, gray block, cyan block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block is in the brown box']. The remaining goal is ['Put blue block, gray block, cyan block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block and a blue block are in the brown box']. The remaining goal is ['Put gray block, cyan block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink and blue blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the pink and blue blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the pink and blue blocks are not in the brown box; the current progress is ['The gray block is in the brown box']. The task feasibility is unaffected since the remaining target objects [pink block, blue block, cyan block, green block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the pink and blue blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block and a gray block are in the brown box']. The remaining goal is ['Put the blue block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The progress is ['Pink block, blue block, and gray block are in the brown box']. The remaining goal is ['Put cyan and green blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the pink, blue, and gray blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the pink, blue, and gray blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the pink, blue, and gray blocks are not in the brown box; the current progress is ['The cyan block is in the brown box']. The task feasibility is unaffected since the remaining target objects [pink block, blue block, gray block, green block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the pink, blue, and gray blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A pink block and a cyan block are in the brown box']. The remaining goal is ['Put the blue block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Pink block, blue block, and cyan block are in the brown box']. The remaining goal is ['Put gray and green blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the gray block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The current progress is ['Pink block, blue block, gray block, and cyan block are in the brown box']. The remaining goal is ['Put the green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Pink block, blue block, gray block, cyan block, and green block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
                )

            episode_3=(
                "### User:\n"+
                "In the initial state, there are orange, purple, red, blue, and yellow blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Orange block, purple block, red block, blue block, and yellow block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['An orange block is in the brown box']. The remaining goal is ['Put purple block, red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['An orange block and a purple block are in the brown box']. The remaining goal is ['Put red block, blue block, and yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the orange and purple blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the orange and purple blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the orange and purple blocks are not in the brown box; the current progress is ['The red block is in the brown box']. The task feasibility is unaffected since the remaining target objects [orange block, purple block, blue block, yellow block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the orange and purple blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['An orange block and a red block are in the brown box']. The remaining goal is ['Put the purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The current progress is ['Orange block, purple block, and red block are in the brown box']. The remaining goal is ['Put blue and yellow blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the orange, purple, and red blocks in the brown box are moved to other positions on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the orange, purple, and red blocks in the brown box are moved to other positions on the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress is disrupted, and the orange, purple, and red blocks are not in the brown box; the current progress is ['The blue block is in the brown box']. The task feasibility is unaffected since the remaining target objects [orange block, purple block, red block, yellow block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the orange, purple, and red blocks back in the brown box to resume progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['An orange block and a blue block are in the brown box']. The remaining goal is ['Put the purple block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Orange block, purple block, and blue block are in the brown box']. The remaining goal is ['Put red and yellow blocks in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. The current progress is ['Orange block, purple block, red block, and blue block are in the brown box']. The remaining goal is ['Put the yellow block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['Orange block, blue block, purple block, red block, and yellow block are in the brown box']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3]
        elif anomaly_type=="removal":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, gray, white, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, pink block, gray block, white block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A cyan block is in the brown box']. The remaining goal is ['Put pink block, gray block, white block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"
                "### User:\n"+
                "The action succeeded, and the white block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the white block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A cyan block and a pink block are in the brown box'] is unaffected; the task feasibility is affected since the disappeared white block is among the remaining target objects [gray block, white block, green block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "The task feasibility is affected.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "alert.\n" )
            
            episode_2=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, gray, white, and green blocks; there is a brown box and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "The final goal state is ['Cyan block, pink block, gray block, white block, and green block are in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The progress is ['A cyan block is in the brown box']. The remaining goal is ['Put pink block, gray block, white block, and green block in the brown box'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block in the brown box.\n"+
                "### User:\n"+
                "The action succeeded, and the white block on the table disappeared.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the white block on the table disappeared] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['A cyan block and a pink block are in the brown box'] is unaffected; the task feasibility is affected since the disappeared white block is among the remaining target objects [gray block, white block, green block].\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "The task feasibility is affected.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "alert.\n"
            )

            anomaly_episode_list=[episode_1,episode_2]
    elif "pyramid" in task:
        if  anomaly_type=="addition":
            episode_1=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the red, blue, and green blocks are in the bottom row; the yellow and orange blocks are in the middle row; the pink block is in the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a red block is on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen purple block appears at the top right.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen purple block appears at the top right] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['The red and blue blocks are on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, orange block, pink block] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The robot will not be affected since the anomaly block [purple block at the top right] is not a target object and has a different color from any target blocks.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block on the red and blue blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen pink block appears at the bottom left.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen pink block appears at the bottom left] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['The bottom row (red, blue, and green blocks) is built, and the yellow block is on top of the bottom row'] is unaffected; the task feasibility is unaffected since the remaining target objects [orange block, pink bowl] are still available.\n" +
                "### User:\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n"
                "The robot may mistake the anomaly block [pink block at the bottom left] for the target pink block since they have the same color.\n" +
                "### User:\n"
                "How to handle this anomaly?\n" +
                "### Assistant:\n"
                "Remove the anomaly block to prevent confusion.\n" +
                "### User:\n"
                "What is your plan for the next step?\n" +
                "### Assistant:\n"
                "put the pink block at the bottom left into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The yellow block is on the built bottom row (red, blue, and green blocks)']. Remaining goals: ['put the orange block on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) and the middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top right.\n"+
                "### User:\n"
                "Analyze the effect of the anomaly [a never-seen gray block appears at the top right] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n"
                "The progress ['The bottom row (red, blue, and green blocks), the middle row (yellow and orange blocks), and the top row (the pink block) are built'] is unaffected; the task feasibility is unaffected since there is no target object left and all goals are completed.\n"
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected since the anomaly block [gray block appears at the top right] is not a target object and all goals are completed.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n")

            episode_2=(
                "### User:\n"+
                "In the initial state, there are blue, green, yellow, red, orange, pink, purple, and gray blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the blue, green, and yellow blocks make the bottom row; the red and orange blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen gray block appears at the top left.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen gray block appears at the top left] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['a blue block is on the stand'] is unaffected; the task feasibility is unaffected since the remaining target objects [green block, yellow block, red block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected since the anomaly block [gray block at the top left] is not a target object and has a different color from any target blocks.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "No action needed\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and green blocks are on the stand']. Remaining goals: ['put the yellow block on the stand to make the bottom row'; 'put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and a never-seen red block appears at the bottom right.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [a never-seen red block appears at the bottom right] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "The progress ['The bottom row (blue, green, and yellow blocks) is built'] is unaffected; the task feasibility is unaffected since the remaining target objects [red block, orange block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot may mistake the anomaly block [red block at the bottom right] for the target red block since they have the same color.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Remove the anomaly block to prevent confusion.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block at the bottom right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, green, and yellow blocks) is built']. Remaining goals: ['put the red and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, green, and yellow blocks) is built, and and the red block) is on top of the bottom row']. Remaining goals: ['put the orange block on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block on the green and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, green, and yellow blocks) and the middle row (red and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, green, and yellow blocks), the middle row (red and orange blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_3=(
                "### User:\n"+
                "In the initial state, there are yellow, blue, red, green, orange, white, and pink blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the yellow, blue, and red blocks make the bottom row; the green and orange blocks make the middle row; the white block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a yellow block is on the stand']. Remaining goals: ['put the blue and red blocks on the stand to make the bottom row'; 'put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n" +
                "### Assistant:\n"
                "put the cyan block on the darkest brown block of the stand into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The yellow and blue blocks are on the stand']. Remaining goals: ['put the red block on the stand to complete the bottom row'; 'put the green and orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks) is built']. Remaining goals: ['put the green and orange blocks on the bottom row to make the middle row'; 'put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n" +
                "### Assistant:\n"
                "put the pink block on the blue and red blocks into the trash can.\n" +
                "### User:\n"
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n"
                "Please describe The progress and the remaining goals.\n" +
                "### Assistant:\n"
                "The anomaly has been addressed. Progress: ['The bottom row (yellow, blue, and red blocks) is built, and the green block is on top of the bottom row']. Remaining goals: ['put the orange blocks on top of the bottom row to make the middle row'; 'put the white block on top of the middle row to make the top row'].\n" +
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and red blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks) and the middle row (green and orange blocks) are built']. Remaining goals: ['put the white block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block on the green and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (yellow, blue, and red blocks), the middle row (green and orange blocks), and the top row (the white block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_4=(
                "### User:\n"+
                "In the initial state, there are red, blue, green, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the red, blue, and green blocks make the bottom row; the yellow and orange blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block on the middle brown block of the stand into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['a red block is on the stand']. Remaining goals: ['put the blue and green blocks on the stand to make the bottom row'; 'put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The red and blue blocks are on the stand']. Remaining goals: ['put the green block on the darkest brown block of the stand to complete the bottom row'; 'put the yellow and orange blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block on the red and blue blocks into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (red, blue, and green blocks) is built']. Remaining goals: ['put the yellow and orange blocks on the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the blue and green blocks into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (red, blue, and green blocks) is built, and the yellow block is on top of the bottom row']. Remaining goals: ['put the orange block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block on the blue and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks) and the middle row (yellow and orange blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the yellow and orange blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (red, blue, and green blocks), the middle row (yellow and orange blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_5=(
                "### User:\n"+
                "In the initial state, there are cyan, pink, gray, white, green, orange, and yellow blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the cyan, pink, and gray blocks make the bottom row; the white and green blocks make the middle row; the orange block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the cyan block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['a cyan block is on the stand']. Remaining goals: ['put the pink and gray blocks on the stand to make the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The cyan and pink blocks are on the stand']. Remaining goals: ['put the gray block on the darkest brown block of the stand to complete the bottom row'; 'put the white and green blocks on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
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
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the stand at the top right into the trash can.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (cyan, pink, and gray blocks) is built']. Remaining goals: ['put the white block on the bottom row to make the middle row'; 'put the green block on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the white block on the cyan and pink blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks) is built, and the white block is on top of the bottom row']. Remaining goals: ['put the green block on the bottom row to make the middle row'; 'put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the pink and gray blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks) and the middle row (white and green blocks) are built']. Remaining goals: ['put the orange block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the orange block on the white and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (cyan, pink, and gray blocks), the middle row (white and green blocks), and the top row (the orange block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            
            anomaly_episode_list=[episode_2,episode_3,episode_4,episode_5]
        elif anomaly_type=="removal":
            episode_1 = (
                "### User:\n" +
                "In the initial state, there are red, green, blue, yellow, orange, pink, purple, and gray blocks; there is a stand and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Final goal state: ['The red, green, and blue blocks make the bottom row; the yellow and orange blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the red block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A red block is on the stand']. The remaining goals are ['Put the green and blue blocks on the stand to make the bottom row'; 'Put the yellow and orange blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the green block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the orange block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The red and green blocks are on the stand'] is unaffected; the task feasibility is unaffected since the disappeared orange block is among the remaining target objects [blue block, yellow block, orange block, pink block].\n" 
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert since the task feasibility is affected.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            episode_2 = (
                "### User:\n" +
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and gray blocks; there is a stand and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Final goal state: ['The blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the blue block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A blue block is on the stand']. The remaining goals are ['Put the yellow and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the yellow block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the orange block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the orange block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['A blue block and a yellow block are on the stand'] is unaffected; the task feasibility is unaffected since the disappeared orange block is not among the remaining target objects [green block, red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the green block on the darkest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the red block on the blue and yellow blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) and the middle row (red block) are built']. Remaining goals: ['Put the purple block on the middle row to complete it'; 'Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the purple block on the yellow and green blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['Put the pink block on the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the pink block on the red and purple blocks.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "done.\n"
            )

            episode_3 = (
                "### User:\n" +
                "In the initial state, there are cyan, white, green, red, purple, pink, yellow, and gray blocks; there is a stand and a trash can.\n" +
                "What is the final goal state?\n" +
                "### Assistant:\n" +
                "Final goal state: ['The cyan, white, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the cyan block on the lightest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and no anomaly happened.\n" +
                "### User:\n" +
                "Please describe the achieved progress and the remaining goals.\n" +
                "### Assistant:\n" +
                "The progress is ['A cyan block is on the stand']. The remaining goals are ['Put the white and green blocks on the stand to make the bottom row'; 'Put the red and purple blocks on top of the bottom row to make the middle row'; 'Put the pink block on top of the middle row to make the top row'].\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the white block on the middle brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the yellow block on the table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the yellow block on the table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['A cyan block and a white block are on the stand'] is unaffected; the task feasibility is unaffected since the disappeared yellow block is not among the remaining target objects [green block, red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "No action needed.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "put the green block on the darkest brown block of the stand.\n" +
                "### User:\n" +
                "The action succeeded, and the purple block on table disappears.\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly [the purple block on table disappears] on the task regarding progress and feasibility.\n" +
                "### Assistant:\n" +
                "The progress ['The bottom row (blue, yellow, and green blocks) is built'] is unaffected; the task feasibility is affected since the disappeared purple block is among the remaining target objects [red block, purple block, pink block].\n" +
                "### User:\n" +
                "Analyze the effect of the anomaly on future actions.\n" +
                "### Assistant:\n" +
                "The robot will not be affected.\n" +
                "### User:\n" +
                "How to handle this anomaly?\n" +
                "### Assistant:\n" +
                "Need to alert since the task feasibility is affected.\n" +
                "### User:\n" +
                "What is your plan for the next step?\n" +
                "### Assistant:\n" +
                "alert.\n"
            )
            anomaly_episode_list=[episode_1,episode_2,episode_3]
        elif anomaly_type=="displcement":
            episode_1 = (
                "### User:\n"+
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and brown blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and the blue block on the stand is amoved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the blue block on the stand amoved to another position on the table.] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the blue block used to make the bottom row is moved to another position on the table. The current progress is ['the yellow block is on the middle brown block of the stand']; the task feasibility is unaffected since the remaining target objects [blue block, green block, red block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the blue block back to the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The blue and yellow blocks are on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and the green block on the stand is amoved to another position on the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the green block on the stand is amoved to another position on the table.] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the green block used to make the bottom row is moved to another position on the table. The current progress is ['the blue and yellow blocks are on the stand']; the task feasibility is unaffected since the remaining target objects [green block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the green block back to the the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            episode_2 = (
                "### User:\n"+
                "In the initial state, there are blue, yellow, green, red, purple, pink, orange, and brown blocks; there is a stand and a trash can.\n"+
                "What is the final goal state?\n"+
                "### Assistant:\n"+
                "Final goal state: ['the blue, yellow, and green blocks make the bottom row; the red and purple blocks make the middle row; the pink block makes the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "Progress: ['A blue block is on the stand']. Remaining goals: ['put the yellow and green blocks on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and yellow blocks are on the stand']. Remaining goals: ['put the green block on the stand to make the bottom row'; 'put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the green block on the darkest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and the blue and yellow blocks on the stand are moved to other positions of the table.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly [the blue and yellow blocks on the stand are moved to other positions of the table] on the task regarding progress and feasibility.\n"+
                "### Assistant:\n"+
                "Progress is disrupted, and the blue and yellow blocks used to make the bottom row are moved to other positions. The current progress is ['A green block is on the stand']; the task feasibility is unaffected since the remaining target objects [blue block, yellow block, red block, purple block, pink block] are still available.\n"+
                "### User:\n"+
                "Analyze the effect of the anomaly on future actions.\n"+
                "### Assistant:\n"+
                "The robot will not be affected.\n"+
                "### User:\n"+
                "How to handle this anomaly?\n"+
                "### Assistant:\n"+
                "Put the blue and yellow blocks back to the stand to resume the progress.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the blue block on the lightest brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The blue and green blocks are on the stand']. To address this anomaly, the remaining goal is ['put the yellow block on the middle brown block of the stand'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the yellow block on the middle brown block of the stand.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "The anomaly has been addressed. Progress: ['The bottom row (blue, yellow, and green blocks) is built']. Remaining goals: ['put the red and purple blocks on top of the bottom row to make the middle row'; 'put the pink block on top of the middle row to make the top row']\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the red block on the blue and yellow blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) is built, and the red block is on top of the bottom row']. Remaining goals: ['put the purple block on top of the bottom row to make the middle row'; 'put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the purple block on the yellow and green blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks) and the middle row (red and purple blocks) are built']. Remaining goals: ['put the pink block on the middle row to make the top row'].\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "put the pink block on the red and purple blocks.\n"+
                "### User:\n"+
                "The action succeeded, and no anomaly happened.\n"+
                "### User:\n"+
                "Please describe the achieved progress and the remaining goals.\n"+
                "### Assistant:\n"+
                "Progress: ['The bottom row (blue, yellow, and green blocks), the middle row (red and purple blocks), and the top row (the pink block) are built']. All goals are completed.\n"+
                "### User:\n"+
                "What is your plan for the next step?\n"+
                "### Assistant:\n"+
                "done.\n"
            )

            anomaly_episode_list=[episode_1,episode_2]
        
        
    return anomaly_episode_list    