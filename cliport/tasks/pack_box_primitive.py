import random
from typing import List, Set, Union

import numpy as np
import pybullet as p
import os
from cliport.tasks.task import Task
from cliport.utils import utils

rel_postion = ['top left', 'top right', 'bottom left', 'bottom right']



class PackBoxPrimitive(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_steps = 1
        self.task_name="pack-box-primitive"
        self.task_completed_desc = "done packing boxes."
        self.answer_template = "The action succeed, and "
        self.obj_colors = {}

    def reset(self, env):
        super().reset(env)


        lang_template = "put the {pick_color} block in the brown box"
        question_template = "Did the robot successfully execute the action 'put the {pick_color} block in the brown box', and did any anomaly happen?"

        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        env.add_object(container_template, trashcan_pose, 'fixed')

        # Add container box.

        zone_size = self.get_random_size(0.05, 0.3, 0.05, 0.3, 0.05, 0.05)
        zone_pose = self.get_random_pose(env, zone_size)
        container_template = 'container/container-template.urdf'
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        container_urdf = self.fill_template(container_template, replace)
        env.add_object(container_urdf, zone_pose, 'fixed')

        os.remove(container_urdf)

        self.zone_size = zone_size
        self.zone_pose = zone_pose
        margin = 0.01
        min_object_dim = 0.05

        bboxes = []

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

        colors = [utils.COLORS[c] for c in utils.COLORS if c != 'brown']
        color_names = list(utils.COLORS.keys())
        color_names.remove('brown')
        # Add objects in container.
        object_points = {}
        object_ids = []
        object_colors = {}
        bboxes = np.array(bboxes)
        object_template = 'box/box-template.urdf'

        for bbox in bboxes:
            size = bbox[3:] - bbox[:3]
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2
            pose = (position, (0, 0, 0, 1))
            pose = utils.multiply(zone_pose, pose)
            urdf = self.fill_template(object_template, {'DIM': size})
            box_id = env.add_object(urdf, pose)
            os.remove(urdf)
            object_ids.append((box_id, (0, None)))
            icolor = np.random.choice(range(len(colors)), 1).squeeze()
            p.changeVisualShape(box_id, -1, rgbaColor=colors[icolor] + [1])
            object_colors[box_id] = color_names[icolor]
        # Randomly select object in box and save ground truth pose.
        self.inside_box_blocks={}
        object_volumes = []
        true_poses = {}
        nbr_outside_boxes = random.randint(1, len(object_ids))
        outside_boxes_objs = object_ids[-nbr_outside_boxes:]
        inside_boxes_objs=list(set(object_ids)-set(outside_boxes_objs))
        for id, _ in inside_boxes_objs:
            self.inside_box_blocks[id]=object_colors[id]
        outside_obj_ids = []
        for object_id, _ in outside_boxes_objs:
            # print("fuck")
            true_pose = p.getBasePositionAndOrientation(object_id)
            object_size = p.getVisualShapeData(object_id)[0][3]
            object_volumes.append(np.prod(np.array(object_size) * 100))
            pose = self.get_random_pose(env, object_size)
            p.resetBasePositionAndOrientation(object_id, pose[0], pose[1])
            true_poses[object_id] = true_pose
            outside_obj_ids.append(object_id)
        goal_obj_id = outside_obj_ids[0]
        object_points[goal_obj_id] = self.get_object_points(goal_obj_id)

        # if target=="brown box":
        self.goals.append((
            [(goal_obj_id, (0, None))], np.eye(1), [true_poses[goal_obj_id]], False, True, 'zone',
            (object_points, [(zone_pose, zone_size)]), 1))
        true_poses.pop(goal_obj_id)
        self.remain_container_poses=true_poses
        self.remain_obj_info=[]
        for id in outside_obj_ids:
            if id !=goal_obj_id:
                self.remain_obj_info.append((id,object_colors[id]+" block"))

        self.lang_goals.append(lang_template.format(pick_color=object_colors[goal_obj_id]))
        self.question_list.append(question_template.format(pick_color=object_colors[goal_obj_id]))
        self.answer_list.append(self.answer_template)

        self.obj_colors['blocks'] = [name for _, name in object_colors.items()]
        self.obj_colors['box'] = "brown"

        return True




class PackBoxwithRelativePickPosition(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_steps = 1
        self.lang_template = "put the {pick_obj} {pick_position} into the trash can"
        self.task_completed_desc = "done packing boxes."
        self.question_template = "Did the robot successfully execute the action 'put the {pick_obj} {pick_position} into the trash can', and did any anomaly happen?"
        self.answer_template = "The action succeed, and "
        self.task_name="pack-box-relative-primitive"
    def reset(self, env):
        super().reset(env)

        trashcan_pose = ((0.35, random.choice([-0.38, 0.38]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')
        trashcan_size = p.getVisualShapeData(trashcan_id)[0][3]
        target=random.choice(["blockinzone","blockinbox","brown box"])

        while True:
            container_pos = random.sample(rel_postion, 2)
            # Add container box.
            zone_size = self.get_random_size(0.05, 0.3, 0.05, 0.3, 0.05, 0.05)
            zone_pose = self.get_random_pose(env, zone_size, container_pos[0])
            if None in zone_pose:
                continue
            container_template = 'container/container-template.urdf'
            half = np.float32(zone_size) / 2
            replace = {'DIM': zone_size, 'HALF': half}
            container_urdf = self.fill_template(container_template, replace)
            env.add_object(container_urdf, zone_pose, 'fixed')

            os.remove(container_urdf)

            self.zone_size = zone_size
            self.zone_pose = zone_pose
            margin = 0.01
            min_object_dim = 0.05
            bboxes = []
            bboxes = []

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

            colors = [utils.COLORS[c] for c in utils.COLORS if c != 'brown']
            color_names = list(utils.COLORS.keys())
            color_names.remove('brown')
            # Add objects in container.
            object_ids = []
            object_colors = {}

            object_template = 'box/box-template.urdf'

            for bbox in bboxes:
                size = bbox[3:] - bbox[:3]
                position = size / 2. + bbox[:3]
                position[0] += -zone_size[0] / 2
                position[1] += -zone_size[1] / 2
                pose = (position, (0, 0, 0, 1))
                pose = utils.multiply(zone_pose, pose)
                urdf = self.fill_template(object_template, {'DIM': size})
                box_id = env.add_object(urdf, pose)
                os.remove(urdf)
                object_ids.append((box_id, (0, None)))
                icolor = np.random.choice(range(len(colors)), 1).squeeze()
                p.changeVisualShape(box_id, -1, rgbaColor=colors[icolor] + [1])
                object_colors[box_id] = color_names[icolor]


            self.un_finished_goal_poses = {}
            # Randomly select object in box and save ground truth pose.
            nbr_outside_boxes = random.randint(1, len(object_ids))
            outside_boxes_objs = object_ids[-nbr_outside_boxes:]
            #print(len(outside_boxes_objs))
            for object_id, _ in outside_boxes_objs:
                true_pose = p.getBasePositionAndOrientation(object_id)
                object_size = p.getVisualShapeData(object_id)[0][3]
                self.un_finished_goal_poses[object_id]=(true_pose,object_size)
                pose = self.get_random_pose(env, object_size)
                if None in pose:
                    return None
                p.resetBasePositionAndOrientation(object_id, pose[0], pose[1])
                #print("fuck")
            break
        #print("fuck")
        ## add confusing container
        if target=="brown box":
            i=0
            while i<50:
                zone_size = (0.08,0.08,0.05)
                adv_zone_pose = self.get_random_pose(env, zone_size, container_pos[1])

                container_template = 'container/container-template.urdf'
                half = np.float32(zone_size) / 2
                replace = {'DIM': zone_size, 'HALF': half}
                container_urdf = self.fill_template(container_template, replace)
                adv_obj_id = env.add_object(container_urdf, adv_zone_pose)
                if adv_obj_id is not None:
                    break
                i+=1
            if adv_obj_id == None:
                return None
            pick_obj_name = "brown box"
            pick_pos="at the "+container_pos[1]
        elif target=="blockinbox":
            while True:
                obj_id,__=random.choice(list(outside_boxes_objs))
                pose,size=self.un_finished_goal_poses[obj_id]
                color_idx = random.sample(range(len(color_names)),1)[0]
                color=color_names[color_idx]
                urdf = self.fill_template(object_template, {'DIM': size})
                adv_obj_id = env.add_object(urdf, pose)
                p.changeVisualShape(adv_obj_id, -1, rgbaColor=colors[color_idx] + [1])
                if adv_obj_id is not None:
                    break
            pick_obj_name=color+" block"
            pick_pos="in the brown box"
        else:
            obj_id,__=random.choice(list(outside_boxes_objs))
            __,size=self.un_finished_goal_poses[obj_id]
            urdf = self.fill_template(object_template, {'DIM': size})
            adv_obj_id,adv_pos = self.add_adv_object(obj_id,urdf,size,env)
            color_value = p.getVisualShapeData(obj_id)[0][-1]
            p.changeVisualShape(adv_obj_id, -1, rgbaColor=color_value)
            if adv_obj_id is None:
                return None
            pick_obj_name = object_colors[obj_id] + " block"
            pick_pos = "at the "+adv_pos
        obj_points = {adv_obj_id: self.get_object_points(trashcan_id)}
        obj_ids=[]
        obj_ids.append((adv_obj_id, (0, None)))
        self.goals.append((
            obj_ids,np.eye(1), [trashcan_pose], False, False, 'trash',(obj_points,[(trashcan_pose,trashcan_size)]) , 1))

        self.lang_goals.append(self.lang_template.format(pick_obj=pick_obj_name,pick_position=pick_pos))
        self.question_list.append(self.question_template.format(pick_obj=pick_obj_name,pick_position=pick_pos))
        self.answer_list.append(self.answer_template)

        return True


    def add_adv_object(self,obj_id, urdf,object_size,env):
        #print(self.get_object_points(obj_id))
        true_pose = p.getBasePositionAndOrientation(obj_id)
        current_pos=self.determine_region(true_pose[0])
        i=0
        rel_pos = ['top left', 'top right', 'bottom left', 'bottom right']
        rel_pos.remove(current_pos)
        while i<20:
            adv_pos = random.choice(rel_pos)
            pose = self.get_random_pose(env, object_size, zone=adv_pos)
            adv_obj_id = env.add_object(urdf, pose)

            if adv_obj_id is not None:
                return adv_obj_id, adv_pos
            i+=1
        return None
    
    

class PackBoxPrimitiveaAnomaly(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_steps = 1
        self.task_name="pack-box-primitive"
        self.task_completed_desc = "done packing boxes."
        self.answer_template = "The action succeed, and "
        self.obj_colors = {}

    def reset(self, env):
        super().reset(env)


        lang_template = "put the {pick_color} block in the brown box"
        question_template = "Did the robot successfully execute the action 'put the {pick_color} block in the brown box', and did any anomaly happen?"

        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        env.add_object(container_template, trashcan_pose, 'fixed')

        # Add container box.

        zone_size = self.get_random_size(0.05, 0.3, 0.05, 0.3, 0.05, 0.05)
        zone_pose = self.get_random_pose(env, zone_size)
        container_template = 'container/container-template.urdf'
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        container_urdf = self.fill_template(container_template, replace)
        env.add_object(container_urdf, zone_pose, 'fixed')

        os.remove(container_urdf)

        self.zone_size = zone_size
        self.zone_pose = zone_pose
        margin = 0.01
        min_object_dim = 0.05

        bboxes = []

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
        object_points = {}
        object_ids = []
        object_colors = {}
        self.object_colors = {}
        bboxes = np.array(bboxes)
        object_template = 'box/box-template.urdf'

        for bbox in bboxes:
            size = bbox[3:] - bbox[:3]
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2
            pose = (position, (0, 0, 0, 1))
            pose = utils.multiply(zone_pose, pose)
            urdf = self.fill_template(object_template, {'DIM': size})
            box_id = env.add_object(urdf, pose)
            os.remove(urdf)
            object_ids.append((box_id, (0, None)))
            icolor = np.random.choice(range(len(relevant_color_names)), 1).squeeze()
            p.changeVisualShape(box_id, -1, rgbaColor=pack_colors[icolor] + [1])
            object_colors[box_id] = relevant_color_names[icolor]
        # Randomly select object in box and save ground truth pose.
        self.inside_box_blocks={}
        object_volumes = []
        true_poses = {}
        nbr_outside_boxes = random.randint(1, len(object_ids))
        outside_boxes_objs = object_ids[-nbr_outside_boxes:]
        inside_boxes_objs=list(set(object_ids)-set(outside_boxes_objs))
        for id, _ in inside_boxes_objs:
            self.inside_box_blocks[id]=object_colors[id]
        outside_obj_ids = []
        for object_id, _ in outside_boxes_objs:
            # print("fuck")
            true_pose = p.getBasePositionAndOrientation(object_id)
            object_size = p.getVisualShapeData(object_id)[0][3]
            object_volumes.append(np.prod(np.array(object_size) * 100))
            pose = self.get_random_pose(env, object_size)
            p.resetBasePositionAndOrientation(object_id, pose[0], pose[1])
            true_poses[object_id] = true_pose
            outside_obj_ids.append(object_id)
        goal_obj_id = outside_obj_ids[0]
        object_points[goal_obj_id] = self.get_object_points(goal_obj_id)


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


        # if target=="brown box":
        self.goals.append((
            [(goal_obj_id, (0, None))], np.eye(1), [true_poses[goal_obj_id]], False, True, 'zone',
            (object_points, [(zone_pose, zone_size)]), 1))
        true_poses.pop(goal_obj_id)
        self.remain_container_poses=true_poses
        self.remain_obj_info=[]
        for id in outside_obj_ids:
            if id !=goal_obj_id:
                self.remain_obj_info.append((id,object_colors[id]+" block"))

        self.lang_goals.append(lang_template.format(pick_color=object_colors[goal_obj_id]))
        self.question_list.append(question_template.format(pick_color=object_colors[goal_obj_id]))
        self.answer_list.append(self.answer_template)

        self.obj_colors['blocks'] = [name for _, name in object_colors.items()]
        self.obj_colors['box'] = "brown"

        return True
