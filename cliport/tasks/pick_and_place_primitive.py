import random
from typing import List, Set, Union

import numpy as np
import pybullet as p
import os
from cliport.tasks.task import Task
from cliport.utils import utils

rel_postion = ['top left', 'top right', 'bottom left', 'bottom right']


class PickAndPlacePrimitive(Task):
    """
    Pick-and-place primitive for the LLM planner.
    This primitive is trained with all the colors, following the setting of `Inner Monologue`.
    Pick up the [block1] and place it on the [block2/bowl/zone].
    """

    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.task_name="pick-block-primitive"
        self.pos_eps = 0.05
        self.task_completed_desc = "done placing blocks."
        self.answer_template = "The action is executed successfully and"
        self.obj_colors = {}

    def reset(self, env):
        super().reset(env)
        target = random.choice(["bowl", "trash can"])


        lang_template = "put the {pick_color} block {positional_word} the {place_obj}"
        question_template = "Did the robot successfully execute the action 'put the {pick_color} block {positional_word} the {place_obj}', and did any anomaly happen?"

        all_color_names = self.get_colors()

        n_blocks = np.random.randint(2, 4)
        n_bowls = np.random.randint(2, 4)

        block_colors = random.sample(all_color_names, n_blocks)
        bowl_colors = random.sample(all_color_names, n_bowls)
        block_util_colors = [utils.COLORS[cn] for cn in block_colors]
        bowl_util_colors = [utils.COLORS[cn] for cn in bowl_colors]

        # add trash can
        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))

        container_template = 'trash_can/trashcan.urdf'
        trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')
        trashcan_size = p.getVisualShapeData(trashcan_id)[0][3]

        # Add bowls.
        bowl_size = (0.12, 0.12, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        bowl_poses = []
        bowl_id_list=[]
        for i in range(n_bowls):
            bowl_pose = self.get_random_pose(env, bowl_size)
            bowl_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
            p.changeVisualShape(bowl_id, -1, rgbaColor=bowl_util_colors[i] + [1])
            bowl_poses.append(bowl_pose)
            bowl_id_list.append(bowl_id)

        # Add blocks.
        blocks = []
        block_pts = {}
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        place_pose = None
        block_id_list=[]
        for i in range(n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=block_util_colors[i] + [1])
            if i == 0:
                block_pts[block_id] = self.get_box_object_points(block_id)
            elif i == 1:
                place_pose = block_pose
            if target in ['bowl','trash can']:
                blocks.append((block_id, (0, None)))
            else:
                blocks.append((block_id, (np.pi / 2, None)))
            block_id_list.append(block_id)
        pick_color=block_colors[0]
        #print(target)
        if target == "trash can":
            adv_obj_id, __ = blocks[0]
            obj_points = {adv_obj_id: self.get_object_points(trashcan_id)}
            obj_ids = []
            obj_ids.append((adv_obj_id, (0, None)))
            self.goals.append((
                obj_ids, np.eye(1), [trashcan_pose], True, False, 'zone',
                (obj_points, [(trashcan_pose, trashcan_size)]), 1))


            place_obj="trash can"
            positional_word="into"
        else:
            if target == "block":
                target_pose = (
                    (place_pose[0][0], place_pose[0][1], block_size[2] * 2),
                    place_pose[1]
                )
                self.goals.append((blocks[:1], np.eye(1),
                                   [target_pose], False, True, 'pose', None, 1))

                place_obj = block_colors[1]+" block"
                positional_word = "on"
            elif target == "bowl":
                target_matrix = np.ones((1, 1))
                self.goals.append(([blocks[0]], target_matrix,
                                   [bowl_poses[0]], False, True, 'pose', None, 1))
                place_obj = bowl_colors[0]+" bowl"
                positional_word = "in"
        self.remain_container_poses=[]
        self.remain_pick_obj_poses=[]
        for i in range(1,len(bowl_poses)):
            self.remain_container_poses.append((bowl_poses[i],bowl_colors[i]))
        for i in range(1,len(blocks)):
            self.remain_pick_obj_poses.append((block_id_list[i],block_colors[i]))
        lang_template = lang_template.format(pick_color=pick_color,
                                             positional_word=positional_word,
                                             place_obj=place_obj)
        question_template = question_template.format(pick_color=pick_color,
                                                     positional_word=positional_word,
                                             place_obj=place_obj)
        self.question_list.append(question_template)
        self.answer_list.append(self.answer_template)
        self.lang_goals.append(lang_template)

        return True

    def get_colors(self) -> Union[List[str], Set[str]]:
        return set(utils.TRAIN_COLORS + utils.EVAL_COLORS)


class PickAndPlacePrimitiveWithRelativePickPosition(Task):
    """
    Pick-and-place primitive for the stacking&bowl-related tasks.
    This primitive is trained with all the colors, following the setting of `Inner Monologue`.
    In addition, this primitive is trained to discriminate the objects with identical appearances, by detailed relative positional description:
    top left/right zone, bottom left/right zone, in the bowl,.
    Pick up the [color1][block1][position] and place it on the [color2] [block2/bowl].
    Apart from the target pick block, we particularly add an adversarial block (in different positions) for robust training.
    """

    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.task_name="pick-block-relative-primitive"
        self.pos_eps = 0.05
        self.task_completed_desc = "done placing blocks."
        self.answer_template = "The action is executed successfully and"

    def reset(self, env):

        all_color_names = self.get_colors()


        super().reset(env)
        target_place_type = random.choice(["block2trashcan", 'bowl2trashcan', 'blockinbowl2trashcan'])
        lang_template = "put the {pick_obj} {positional_word} the {pick_pos} into the trash can"
        question_template = "Did the robot successfully execute the action 'put the {pick_obj} {positional_word} the {pick_pos} into the trash can', and did any anomaly happen?"

        n_blocks = np.random.randint(2, 3)
        n_bowls = np.random.randint(2, 3)

        bowl_colors = random.sample(all_color_names, n_bowls)
        block_colors = random.sample(all_color_names, n_blocks)

        bowl_util_colors = [utils.COLORS[cn] for cn in bowl_colors]
        block_util_colors = [utils.COLORS[cn] for cn in block_colors]


        trashcan_pose = ((0.30, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')
        trashcan_size = p.getVisualShapeData(trashcan_id)[0][3]
        # Add bowls.
        bowl_size = (0.14, 0.14, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        bowl_poses = []
        for i in range(n_bowls - 1):
            bowl_pose = self.get_random_pose(env, bowl_size)
            bowl_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
            p.changeVisualShape(bowl_id, -1, rgbaColor=bowl_util_colors[i] + [1])
            bowl_poses.append(bowl_pose)

        # Add other blocks.
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        pick_pos = random.sample(rel_postion, 2)
        block_poses = []
        for i in range(n_blocks - 1):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=block_util_colors[i] + [1])
            block_poses.append(block_pose)
        if target_place_type == "block2trashcan":
            adv_info=self.add_adv_objects(env, block_size, block_urdf, 2, block_util_colors[-1])
            if adv_info is None:
                return None
            valid_block_ids, pick_pos = adv_info
            adv_obj_id=valid_block_ids[0]
            pick_obj=block_colors[-1]+ " block"
            place_pos = pick_pos[0]
            position_word="at"
        elif target_place_type == "blockinbowl2trashcan":
            ## add two more blocks with the same color: one in the bowl and the other not
            while True:
                block_pose = self.get_random_pose(env, block_size, pick_pos[i])
                block_id = env.add_object(block_urdf, block_pose)
                if block_id is not None:
                    break
                else:
                    pick_pos = random.sample(rel_postion,2)
            p.changeVisualShape(block_id, -1, rgbaColor=block_util_colors[-1] + [1])

            pose1, pose2 = bowl_poses[0]
            pose1 = list(pose1)
            pose1[2] = 0.020
            pose1 = tuple(pose1)
            adv_obj_id = env.add_object(block_urdf, (pose1, pose2))
            p.changeVisualShape(adv_obj_id, -1, rgbaColor=block_util_colors[-1] + [1])

            pick_obj=block_colors[-1]+" block"
            place_pos = bowl_colors[0]+" bowl"
            position_word="in"
        else:

            adv_info=self.add_adv_objects(env, bowl_size, bowl_urdf, 2, bowl_util_colors[-1])
            if adv_info is None:
                return None
            valid_bowl_ids, pick_pos = adv_info
            adv_obj_id=valid_bowl_ids[0]
            pick_obj=bowl_colors[-1]+" bowl"
            place_pos = pick_pos[0]
            position_word="at"

        obj_points = {adv_obj_id: self.get_object_points(trashcan_id)}
        obj_ids = []
        obj_ids.append((adv_obj_id, (0, None)))
        self.goals.append((
            obj_ids, np.eye(1), [trashcan_pose], True, False, 'zone',
            (obj_points, [(trashcan_pose, trashcan_size)]), 1))

        lang_template = lang_template.format(pick_obj=pick_obj,
                                             positional_word=position_word,
                                             pick_pos=place_pos)
        question_template = question_template.format(pick_obj=pick_obj,
                                            positional_word=position_word,
                                             pick_pos=place_pos)
        self.remain_container_poses=[]
        self.remain_pick_obj_poses=[]
        for i in range(1,len(bowl_poses)):
            self.remain_container_poses.append((bowl_poses[i],bowl_colors[i]))
        for i in range(1,len(block_poses)):
            self.remain_pick_obj_poses.append((block_poses[i],block_colors[i]))
        self.question_list.append(question_template)
        self.lang_goals.append(lang_template)
        self.answer_list.append(self.answer_template)
        return True
    def get_colors(self) -> Union[List[str], Set[str]]:
        return set(utils.TRAIN_COLORS + utils.EVAL_COLORS)

    def add_adv_objects(self, env, size, urdf, nbr_pos, color):
        count=0
        while count<20:
            pick_pos = random.sample(rel_postion, nbr_pos)
            id_list = []
            for i in range(nbr_pos):
                pose = self.get_random_pose(env, size, pick_pos[i])
                id_list.append(env.add_object(urdf, pose))
            if not None in id_list:
                for id in id_list:
                    p.changeVisualShape(id, -1, rgbaColor=color + [1])
                return id_list, pick_pos
            else:
                count+=1
        return None

