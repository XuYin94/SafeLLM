"""Miscellaneous utilities."""

import cv2
import random
import matplotlib
import matplotlib.pyplot as plt
from time import sleep
import PIL
import numpy as np
import utils
import pybullet as p

import os


def build_gt_scene_info(env,output_queue,task):
    if "matching" in task.task_name:
        matching_bowls_scene(env,output_queue,task)
    elif "packing" in task.task_name:
        box_packing_scene(env,output_queue,task)
    # else:
    #     stack_block_pyramid_scene(env,output_queue,task,perturbation,progress,type)
    
def matching_bowls_scene(env, task):
    block_info = task.block_info.copy()  # Object tuple info with [obj_id, color, pose]
    bowl_info = task.bowl_info.copy()
    
    description = []
    
    # Match blocks to bowls
    for block in block_info:
        block_pose = p.getBasePositionAndOrientation(block[0])
        for bowl in bowl_info:
            bowl_pose = p.getBasePositionAndOrientation(bowl[0])
            if task.is_match(block_pose, bowl_pose, 0):
                description.append(f"{block[1]} block is in the {bowl[1]} bowl.")
                bowl_info.remove(bowl)
                block_info.remove(block)
                break  # Move to next block after finding a match
    
    # For remaining unmatched blocks, assign region
    for block in block_info:
        block_pose = p.getBasePositionAndOrientation(block[0])
        region = task.determine_region(block_pose[0])
        description.append(f"{block[1]} block is in the {region}.")
    
    # For remaining unmatched bowls, assign region
    for bowl in bowl_info:
        bowl_pose = p.getBasePositionAndOrientation(bowl[0])
        region = task.determine_region(bowl_pose[0])
        description.append(f"{bowl[1]} bowl is in the {region}.")
    
    return description


def box_packing_scene(env,output_queue,task):
    description=[]
    block_info = task.block_info.copy()  # Object tuple info with [obj_id, color, pose]
    container_info = task.container_info.copy()
    
    
        # Match blocks to bowls
    for block in block_info:
        block_pose = p.getBasePositionAndOrientation(block[0])
        for container_id in container_info:
            container_pose = p.getBasePositionAndOrientation(container_id)
            container_size = p.getVisualShapeData(container_id)[0][3]
            #print("zone_pose", zone_pose)
            world_to_zone = utils.invert(container_pose)
            obj_to_zone = utils.multiply(world_to_zone, block_pose)
            pts = np.float32(utils.apply(obj_to_zone, pts))
            valid_pts = np.logical_and.reduce([
                pts[0, :] > -container_size[0] / 2, pts[0, :] < container_size[0] / 2,
                pts[1, :] > -container_size[1] / 2, pts[1, :] < container_size[1] / 2,
                pts[2, :] < task.zone_bounds[2, 1]])
            if np.sum(np.float32(valid_pts))>0: ## indicate the in-box state
                description.append(f"A {block[1]} block is in the brown box.")
                container_info.remove(container_id)
    
    # For remaining unmatched blocks, assign region
    for block in block_info:
        block_pose = p.getBasePositionAndOrientation(block[0])
        region = task.determine_region(block_pose[0])
        description.append(f"{block[1]} block is in the {region}.")
    
    # For remaining unmatched bowls, assign region
    for container in container_info:
        bowl_pose = p.getBasePositionAndOrientation(container)
        region = task.determine_region(bowl_pose[0])
        description.append(f"A bronw box is in the {region}.")
    
    return description

## can not generate comprhensive text description for complax object rearrangement