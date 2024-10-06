"""Packing task."""

import os

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils
import random
import pybullet as p

class PackingBoxes(Task):
    """Packing task."""

    def __init__(self):
        super().__init__()
        self.max_steps = 20
        self.task_completed_desc = "done packing boxes."
        self.final_goal="put all current-seen blocks in the brown box"
        self.lang_template = "put the {pick_color} block in the brown box."
        self.question_template = "Did the robot successfully execute the action 'put the {pick_color} block in the brown box', and did any anomaly happen?"
        self.answer_template = "The action is executed successfully, and "
        self.task_name="packing-boxes"
        self.zone_bounds = np.array([[0.25, 0.75], [-0.5, 0.5], [0, 0.08]])

    def reset(self, env):
        super().reset(env)
        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.99))
        container_template = 'trash_can/trashcan.urdf'
        env.add_object(container_template, trashcan_pose, 'fixed')


        # Add container box.
        self.container_info=[]
        zone_size = self.get_random_size(0.05, 0.3, 0.05, 0.3, 0.05, 0.05)
        zone_pose = self.get_random_pose(env, zone_size)
        container_template = 'container/container-template.urdf'
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        container_urdf = self.fill_template(container_template, replace)
        container_id=env.add_object(container_urdf, zone_pose, 'fixed')
        self.container_info.append(container_id)
        if os.path.exists(container_urdf):
            os.remove(container_urdf)

        margin = 0.01
        min_object_dim = 0.05

        initial_objects=[]
        bboxes = []
        self.block_info=[]
        class TreeNode:

            def __init__(self, parent, children, bbox):
                self.parent = parent
                self.children = children
                self.bbox = bbox  # min x, min y, min z, max x, max y, max z

        def KDTree(node):
            size = node.bbox[3:] - node.bbox[:3]

            # Choose which axis to split.
            split = size > 2 * min_object_dim
            if np.sum(split) == 0:
                bboxes.append(node.bbox)
                return 
            split = np.float32(split) / np.sum(split)
            split_axis = np.random.choice(range(len(split)), 1, p=split)[0]

            # Split along chosen axis and create 2 children
            cut_ind = np.random.rand() * \
                      (size[split_axis] - 2 * min_object_dim) + \
                      node.bbox[split_axis] + min_object_dim
            child1_bbox = node.bbox.copy()
            child1_bbox[3 + split_axis] = cut_ind - margin / 2.
            child2_bbox = node.bbox.copy()
            child2_bbox[split_axis] = cut_ind + margin / 2.
            node.children = [
                TreeNode(node, [], bbox=child1_bbox),
                TreeNode(node, [], bbox=child2_bbox)
            ]
            KDTree(node.children[0])
            KDTree(node.children[1])

        # Split container space with KD trees.
        stack_size = np.array(zone_size)
        stack_size[0] -= 0.01
        stack_size[1] -= 0.01
        root_size = (0.01, 0.01, 0) + tuple(stack_size)
        root = TreeNode(None, [], bbox=np.array(root_size))
        KDTree(root)
        bboxes = np.array(bboxes)
        if len(bboxes)>8 or len(bboxes)<6:
            return None
        all_color_names = list(utils.COLORS.keys())
        all_color_names.remove('brown')

        relevant_color_names = np.random.choice(all_color_names, min(4, len(bboxes)), replace=False)
        distractor_color_names = [c for c in all_color_names if c not in relevant_color_names]

        pack_colors = [utils.COLORS[c] for c in relevant_color_names]
        distractor_colors = [utils.COLORS[c] for c in distractor_color_names]

        # Add objects in container.
        self.obj_colors={}
        object_points = {}
        object_ids = []

        self.gt_step=len(bboxes)
        object_template = 'box/box-template.urdf'
        target_list=[]
        for bbox in bboxes:
            size = bbox[3:] - bbox[:3]
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2
            pose = (position, (0, 0, 0, 1))
            pose = utils.multiply(zone_pose, pose)
            urdf = self.fill_template(object_template, {'DIM': size})
            box_id = env.add_object(urdf, pose)
            if os.path.exists(urdf):
                os.remove(urdf)
            object_ids.append((box_id, (0, None)))
            icolor = np.random.choice(range(len(relevant_color_names)), 1).squeeze()
            color_name=relevant_color_names[icolor]
            initial_objects.append(color_name)
            self.block_info.append((box_id,color_name))

            p.changeVisualShape(box_id, -1, rgbaColor=pack_colors[icolor] + [1])
            object_points[box_id] = self.get_box_object_points(box_id)
            target_list.append(icolor)
        # Randomly select object in box and save ground truth pose.
        self.target_color=list(dict.fromkeys(initial_objects))
        true_poses = []
        # self.goal = {'places': {}, 'steps': []}
        for i, (object_id, _) in enumerate(object_ids):
            true_pose = p.getBasePositionAndOrientation(object_id)
            object_size = p.getVisualShapeData(object_id)[0][3]
            pose = self.get_random_pose(env, object_size)
            p.resetBasePositionAndOrientation(object_id, pose[0], pose[1])
            true_poses.append(true_pose)
            assert object_id==self.block_info[i][0]

            self.block_info[i]+=(true_pose,)
        # Add distractor objects
        num_distractor_objects = 4
        distractor_bbox_idxs = np.random.choice(len(bboxes), num_distractor_objects)
        for bbox_idx in distractor_bbox_idxs:
            bbox = bboxes[bbox_idx]
            size = bbox[3:] - bbox[:3]
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2

            pose = self.get_random_pose(env, size)

            urdf = self.fill_template(object_template, {'DIM': size})
            box_id = env.add_object(urdf, pose)

            if os.path.exists(urdf):
                os.remove(urdf)
            icolor = np.random.choice(range(len(distractor_colors)), 1).squeeze()
            if box_id:
                p.changeVisualShape(box_id, -1, rgbaColor=distractor_colors[icolor] + [1])
            self.block_info.append((box_id,distractor_color_names[icolor]))
            initial_objects.append(distractor_color_names[icolor])
        
        #print(self.target_color)
        self.lang_goals.append(self.lang_template)
        self.question_list.append(self.question_template)
        self.answer_list.append(self.answer_template)
        self.goals.append((
            object_ids, np.eye(len(object_ids)), true_poses,
            False, True, 'zone',
            (object_points, [(zone_pose, zone_size)]), 1))
        self.build_initial_scene_description(initial_objects)
        #print(env.obj_ids['fixed'])
        return True

    def build_initial_scene_description(self, initial_objects):
        info = "In the initial state, there are "
        for color in initial_objects[:-1]:
            info += color + ', '
        info += "and " + str(
            initial_objects[-1]) + " blocks; there is a brown box and a trash can.  The instruction is 'Please put all "

        for color in self.target_color[:-1]:
            info += color + ', '
        info+="and "+str(self.target_color[-1])+" blocks in the brown box'."
        #print("fuck")
        self.initial_state = info

