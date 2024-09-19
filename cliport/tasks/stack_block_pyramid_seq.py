"""Stacking Block Pyramid Sequence task."""

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p
import random
rel_postion = ['top left', 'top right', 'bottom left', 'bottom right']


class StackBlockPyramidSeqUnseenColorsPrimitive(Task):
    """ base class."""

    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.gt_step=6
        self.task_name="Stacking Block Pyramid Sequence"
        self.question_template = "Did the robot successfully execute the action 'put the {pick} block on {place}', and did any anomaly happen?"
        self.lang_template = "put the {pick} block on {place}"
        self.task_completed_desc = "done stacking block pyramid."
        self.answer_template = "The action succeeded, and "
    def reset(self, env):
        super().reset(env)
        # add trashcan
        trashcan_pose = ((0.35, random.choice([-0.38, 0.38]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        env.add_object(container_template, trashcan_pose, 'fixed')

        nbr_blocks=random.randint(1,6)

        # Add base.
        base_size = (0.06, 0.18, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose = self.get_random_pose(env, base_size)
        stand_id=env.add_object(base_urdf, base_pose, 'fixed')
        self.container_info=[stand_id,base_pose]

        # Block colors.
        color_names = self.get_colors()
        #print(len(color_names))
        # Shuffle the block colors.
        random.shuffle(color_names)
        colors = [utils.COLORS[cn] for cn in color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'


        # Associate placement locations for goals.
        place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
                     (0, 0.05, 0.03), (0, -0.025, 0.08),
                     (0, 0.025, 0.08), (0, 0, 0.13)]
        targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
        for i in range(nbr_blocks):
            if i ==nbr_blocks-1:
                block_pose = self.get_random_pose(env, block_size)
            else:
                block_pose = targs[i]
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            objs.append((block_id, (np.pi / 2, None)))
        if nbr_blocks==1:
            # Goal: make bottom row.
            block_position="the lightest brown block of the stand"
            self.goals.append(([objs[0]], np.ones((1, 1)), [targs[0]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[0],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[0],
                                                             place=block_position))

        elif nbr_blocks==2:
            block_position="the middle brown block of the stand"
            self.goals.append(([objs[1]], np.ones((1, 1)), [targs[1]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[1],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[1],
                                                             place=block_position))
        elif nbr_blocks==3:
            block_position="the darkest brown block of the stand"
            self.goals.append(([objs[2]], np.ones((1, 1)), [targs[2]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[2],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[2],
                                                             place=block_position))

        elif nbr_blocks==4:
            # Goal: make middle row.
            block_position=f"the {color_names[0]} and {color_names[1]} blocks"
            self.goals.append(([objs[3]], np.ones((1, 1)), [targs[3]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[3],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[3],
                                                             place=block_position))

        elif nbr_blocks==5:
            block_position=f"the {color_names[1]} and {color_names[2]} blocks"
            self.goals.append(([objs[4]], np.ones((1, 1)), [targs[4]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[4],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[4],
                                                             place=block_position))
        else:
            # Goal: make top row.
            block_position=f"the {color_names[3]} and {color_names[4]} blocks"
            self.goals.append(([objs[5]], np.ones((1, 1)), [targs[5]],
                               False, True, 'pose', None, 1))
            self.lang_goals.append(self.lang_template.format(pick=color_names[5],
                                                             place=block_position))
            self.question_list.append(self.question_template.format(pick=color_names[5],
                                                             place=block_position))
        self.answer_list.append(self.answer_template)
        return True
    def get_colors(self):
        return utils.ALL_COLORS




class StackBlockPyramidSeqUnseenColors(Task):
    """ base class."""

    def __init__(self):
        super().__init__()
        self.max_steps = 12
        self.gt_step=6
        self.task_name="Stacking Block Pyramid Sequence"
        self.final_goal="Stack a three-row pyramid with blocks"
        self.question_template = "Did the robot successfully execute the action 'put the {pick} block on {place}', and did any anomaly happen?"
        self.lang_template = "put the {pick} block on {place}"
        self.task_completed_desc = "done stacking block pyramid."
        self.answer_template = "The action succeeded, and "
    def reset(self, env):
        super().reset(env)
        # add trashcan
        trashcan_pose = ((0.35, random.choice([-0.38, 0.38]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        env.add_object(container_template, trashcan_pose, 'fixed')

        nbr_blocks=random.randint(7,9)

        # Add base.
        base_size = (0.06, 0.18, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose = self.get_random_pose(env, base_size)
        stand_id=env.add_object(base_urdf, base_pose, 'fixed')
        self.container_info=[stand_id,base_pose]

        # Block colors.
        all_color_names = self.get_colors()
        random.shuffle(all_color_names)

        colors = [utils.COLORS[c] for c in all_color_names]

        #relevant_color_names = all_color_names[:4]
        target_block_seq =sorted(np.random.choice(range(4), 6, replace=True))
        target_block_colors=[all_color_names[i] for i in target_block_seq]
        target_list=np.unique(target_block_seq)
        self.target_color=[all_color_names[i] for i in target_list]
        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        self.block_info=[]
        for i in range(nbr_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            if i<6:
                p.changeVisualShape(block_id, -1, rgbaColor=colors[target_block_seq[i]] + [1])
                self.block_info.append((block_id, target_block_colors[i]))
            else:
                icolor =np.random.choice(range(4,len(colors)), 1).squeeze()
                p.changeVisualShape(block_id, -1, rgbaColor=colors[icolor] + [1])
                self.block_info.append((block_id, all_color_names[icolor]))
            objs.append((block_id, (np.pi / 2, None)))



        # Associate placement locations for goals.
        place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
                     (0, 0.05, 0.03), (0, -0.025, 0.08),
                     (0, 0.025, 0.08), (0, 0, 0.13)]
        targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
        self.place_list=[]
        # Goal: make bottom row.
        block_position="the lightest brown block of the stand"
        self.goals.append(([objs[0]], np.ones((1, 1)), [targs[0]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[0],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[0],
                                                         place=block_position))

        self.block_info[0]+=(targs[0],block_position,)

        block_position="the middle brown block of the stand"
        self.goals.append(([objs[1]], np.ones((1, 1)), [targs[1]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[1],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[1],
                                                         place=block_position))
        self.block_info[1]+=(targs[1],block_position,)


        block_position="the darkest brown block of the stand"
        self.goals.append(([objs[2]], np.ones((1, 1)), [targs[2]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[2],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[2],
                                                         place=block_position))

        self.block_info[2]+=(targs[2],block_position,)


        # Goal: make middle row.
        block_position=f"the {target_block_colors[0]} and {target_block_colors[1]} blocks"
        self.goals.append(([objs[3]], np.ones((1, 1)), [targs[3]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[3],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[3],
                                                         place=block_position))
        self.block_info[3]+=(targs[3],block_position,)


        block_position=f"the {target_block_colors[1]} and {target_block_colors[2]} blocks"
        self.goals.append(([objs[4]], np.ones((1, 1)), [targs[4]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[4],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[4],
                                                         place=block_position))
        self.block_info[4]+=(targs[4],block_position,)

        # Goal: make top row.
        block_position=f"the {target_block_colors[3]} and {target_block_colors[4]} blocks"
        self.goals.append(([objs[5]], np.ones((1, 1)), [targs[5]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template.format(pick=target_block_colors[5],
                                                         place=block_position))
        self.question_list.append(self.question_template.format(pick=target_block_colors[5],
                                                         place=block_position))
        self.block_info[5]+=(targs[5],block_position,)
        self.answer_list.append(self.answer_template)
        color_list=[item[1] for item in self.block_info]
        self.build_initial_scene_description(color_list,self.target_color)

        return True
    def get_colors(self):
        return utils.ALL_COLORS

    def build_initial_scene_description(self,initial_objects,target_color):
        info = "In the initial state, there are "
        for color in initial_objects[:-1]:
            info+=color+', '
        info+="and "+str(initial_objects[-1])+" blocks; there is a stand and a trash can. The instruction is 'Please stack a pyramid with the "
        for color in target_color[:-1]:
            info += color + ', '
        info+="and "+str(target_color[-1])+" blocks'."
        self.initial_state = info



class StackBlockPyramidSeqSeenColors(StackBlockPyramidSeqUnseenColors):
    def __init__(self):
        super().__init__()

    def get_colors(self):
        return utils.ALL_COLORS


class StackBlockPyramidSeqFull(StackBlockPyramidSeqUnseenColors):
    def __init__(self):
        super().__init__()

    def get_colors(self):
        all_colors = list(set(utils.TRAIN_COLORS) | set(utils.EVAL_COLORS))
        return all_colors


class StackBlockPyramidWithoutSeq(Task):
    """Stacking Block Pyramid without step-by-step instruction base class.
    There is just a high-level instruction: Stack blocks in a pyramid shape """

    def __init__(self):
        super().__init__()
        self.max_steps = 20
        self.lang_template = "stack blocks in a pyramid shape"
        self.task_completed_desc = "done stacking block pyramid."

    def reset(self, env):
        super().reset(env)

        # Add base.
        base_size = (0.05, 0.15, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose = self.get_random_pose(env, base_size)
        env.add_object(base_urdf, base_pose, 'fixed')

        # Block colors.
        color_names = self.get_colors()

        # Shuffle the block colors.
        random.shuffle(color_names)
        colors = [utils.COLORS[cn] for cn in color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(6):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            objs.append((block_id, (np.pi / 2, None)))

        # Associate placement locations for goals.
        place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
                     (0, 0.05, 0.03), (0, -0.025, 0.08),
                     (0, 0.025, 0.08), (0, 0, 0.13)]
        targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]

        # self.goals.append((objs, np.eye(6), targs, False, True, 'pose', None, 1))
        # self.lang_goals.append(self.lang_template)
        # Goal: make bottom row.
        self.goals.append(([objs[0]], np.ones((1, 1)), [targs[0]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[0],
        #                                                  place="the lightest brown block"))
        #
        self.goals.append(([objs[1]], np.ones((1, 1)), [targs[1]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[1],
        #                                                  place="the middle brown block"))
        #
        self.goals.append(([objs[2]], np.ones((1, 1)), [targs[2]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[2],
        #                                                  place="the darkest brown block"))
        #
        # # Goal: make middle row.
        self.goals.append(([objs[3]], np.ones((1, 1)), [targs[3]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[3],
        #                                                  place=f"the {color_names[0]} and {color_names[1]} blocks"))
        #
        self.goals.append(([objs[4]], np.ones((1, 1)), [targs[4]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[4],
        #                                                  place=f"the {color_names[1]} and {color_names[2]} blocks"))
        #
        # # Goal: make top row.
        self.goals.append(([objs[5]], np.ones((1, 1)), [targs[5]],
                           False, True, 'pose', None, 1 / 6))
        self.lang_goals.append(self.lang_template)
        # self.lang_goals.append(self.lang_template.format(pick=color_names[5],
        #                                                  place=f"the {color_names[3]} and {color_names[4]} blocks"))

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS


class StackAllBlock(Task):
    """Stacking ALL Blocks without step-by-step instruction base class.
    There is just a high-level instruction: Stack all blocks. """

    def __init__(self):
        super().__init__()
        self.n_blocks = random.randint(2, 5)
        self.max_steps = self.n_blocks + 2

        self.lang_template = "stack all the blocks"
        self.task_completed_desc = "done stacking block."

    def reset(self, env):
        super().reset(env)

        # Add base.
        base_size = (0.05, 0.15, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose = self.get_random_pose(env, base_size)
        env.add_object(base_urdf, base_pose, 'fixed')

        # Block colors.
        color_names = self.get_colors()

        # Shuffle the block colors.
        random.shuffle(color_names)
        colors = [utils.COLORS[cn] for cn in color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(self.n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            objs.append((block_id, (np.pi / 2, None)))

        self.scene_description = f"On the table, there are {self.n_blocks} blocks. " \
                                 f"Their colors are {color_names[:self.n_blocks]}. "

        # Associate placement locations for goals.
        # place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
        #              (0, 0.05, 0.03), (0, -0.025, 0.08),
        #              (0, 0.025, 0.08), (0, 0, 0.13)]
        place_pos = [(0, 0, 0.03 + 0.05 * i) for i in range(self.n_blocks)]
        # place_pos = [(0, 0, 0.03), (0, 0, 0.08), (0, 0, 0.13)]
        targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]

        match_matrix = np.eye(self.n_blocks)
        # match_matrix = np.ones((self.n_blocks, self.n_blocks))
        self.goals.append((objs, match_matrix, targs, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template)
        # Goal: make bottom row.

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS


class StackAllBlockInAZone(Task):
    """Stacking ALL Blocks In A Zone without step-by-step instruction base class.
    There is just a high-level instruction: Stack all blocks in a zone. """

    def __init__(self):
        super().__init__()
        self.n_blocks = random.randint(2, 5)
        self.max_steps = self.n_blocks + 2

        self.lang_template = "stack all the blocks in the {zone_color} zone"
        self.task_completed_desc = "done stacking block."

    def reset(self, env):
        super().reset(env)

        # Add base.
        base_size = (0.05, 0.15, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose = self.get_random_pose(env, base_size)
        env.add_object(base_urdf, base_pose, 'fixed')

        # Block colors.
        color_names = self.get_colors()

        # Shuffle the block colors.
        random.shuffle(color_names)
        colors = [utils.COLORS[cn] for cn in color_names]
        zone_selected_colors = [c for c in color_names[self.n_blocks:]]
        zone_color_ = random.sample(zone_selected_colors, 1)[0]
        zone_color = utils.COLORS[zone_color_]
        zone_size = (0.15, 0.15, 0)

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(self.n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            objs.append((block_id, (np.pi / 2, None)))

        # Add zones.
        zone_target = zone_pose = self.get_random_pose(env, zone_size)
        zone_obj_id = env.add_object('zone/zone.urdf', zone_pose, 'fixed')
        p.changeVisualShape(zone_obj_id, -1, rgbaColor=zone_color + [1])

        self.scene_description = f"On the table, there are {self.n_blocks} blocks. " \
                                 f"Their colors are {color_names[:self.n_blocks]}. " \
                                 f"There is a zone on the table, and its color is {zone_color_}. "

        # Associate placement locations for goals.
        # place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
        #              (0, 0.05, 0.03), (0, -0.025, 0.08),
        #              (0, 0.025, 0.08), (0, 0, 0.13)]
        place_pos = [(0, 0, 0.03 + 0.05 * i) for i in range(self.n_blocks)]
        # place_pos = [(0, 0, 0.03), (0, 0, 0.08), (0, 0, 0.13)]
        # targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
        targs = [(utils.apply(zone_pose, i), zone_pose[1]) for i in place_pos]

        self.goals.append((objs, np.eye(self.n_blocks), targs, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template.format(zone_color=zone_color_))
        # Goal: make bottom row.

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS


class StackAllBlockOfSameColor(Task):
    """
    Stack ALL Blocks of the same color together.
    There are at most three kinds of color and at most 3 blocks with the same color.
   """

    def __init__(self):
        super().__init__()
        self.n_blocks = random.randint(3, 9)
        self.n_block_colors = random.randint(2, 3)
        self.max_steps = self.n_blocks + 2

        self.lang_template = "stack all the blocks of the same color together"
        self.task_completed_desc = "done stacking block."

    def reset(self, env):
        super().reset(env)

        # Add base.
        base_size = (0.05, 0.15, 0.005)
        base_urdf = 'stacking/stand.urdf'
        base_pose_list = []
        for i in range(self.n_block_colors):
            base_pose = self.get_random_pose(env, base_size)
            base_pose_list.append(base_pose)
            env.add_object(base_urdf, base_pose, 'fixed')

        # Block colors.
        color_names = self.get_colors()
        random.shuffle(color_names)
        block_color_names = random.sample(color_names, self.n_block_colors)
        block_colors = [utils.COLORS[cn] for cn in block_color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(self.n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=block_colors[i % self.n_block_colors] + [1])
            objs.append((block_id, (np.pi / 2, None)))

        self.scene_description = f"On the table, there are {self.n_blocks} blocks, " \
                                 f"and their colors are {block_color_names}."

        # Associate placement locations for goals.
        # place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
        #              (0, 0.05, 0.03), (0, -0.025, 0.08),
        #              (0, 0.025, 0.08), (0, 0, 0.13)]
        # place_pos = [(0, 0, 0.03 + 0.05 * i) for i in range(self.n_blocks)]
        place_pos = [(0, 0, 0.03 + 0.05 * (i // self.n_block_colors)) for i in range(self.n_blocks)]
        # place_pos = [(0, 0, 0.03), (0, 0, 0.08), (0, 0, 0.13)]
        # targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
        targs = [(utils.apply(base_pose_list[i % self.n_block_colors], pos),
                  base_pose_list[i % self.n_block_colors][1]) for i, pos in enumerate(place_pos)]

        match_matrix = np.eye(self.n_blocks)
        # match_matrix = np.ones((self.n_blocks, self.n_blocks))
        self.goals.append((objs, match_matrix, targs, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template)
        # Goal: make bottom row.

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS


class StackBlockWithAlternateColor(Task):
    """Stack all blocks in the form of color crossed, starting from a specific color.
    There are always two kinds of color and at most 3 blocks with the same color.
   """
    # TODO: there are some bugs for creating the demonstrations for this task,
    #  ignore this task at the moment.

    def __init__(self):
        super().__init__()
        self.n_blocks = np.random.randint(2, 5)
        self.n_block_colors = 2
        self.max_steps = self.n_blocks + 2

        self.lang_template = "stack blocks with alternate colors"
        self.task_completed_desc = "done stacking block."

    def reset(self, env):
        super().reset(env)

        # Block colors.
        color_names = self.get_colors()
        block_color_names = random.sample(color_names, self.n_block_colors)
        block_colors = [utils.COLORS[cn] for cn in block_color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        first_block_pose = None
        for i in range(self.n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=block_colors[i % self.n_block_colors] + [1])
            objs.append((block_id, (np.pi / 2, None)))
            if i == 0:
                first_block_pose = block_pose

        goal_poses = []
        for i in range(1, self.n_blocks):
            height = block_size[2] + block_size[2] * i
            goal_poses.append(
                (
                    (first_block_pose[0][0], first_block_pose[0][1], height),
                    first_block_pose[1]
                )
            )

        match_matrix = np.eye(self.n_blocks - 1)
        # match_matrix = np.ones((self.n_blocks, self.n_blocks))
        self.goals.append((objs[1:], match_matrix, goal_poses, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template.format(color=block_color_names[0]))
        # Goal: make bottom row.

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS


class StackBlockPyramidSeqUnseenColorswithrelativepickposition(Task):
    """ base class."""

    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.task_name="Stacking Block Pyramid Sequence"
        self.question_template = "Did the robot successfully execute the action 'put the {pick} block {position} into the trash can', and did any anomaly happen?"
        self.lang_template = "put the {pick} block {position} into the trash can"
        self.task_completed_desc = "done stacking block pyramid."
        self.answer_template = "The action succeeded, and "
    def reset(self, env):
        super().reset(env)

        # add trashcan
        trashcan_pose = ((0.35, random.choice([-0.38, 0.38]), 0.05), (0.0, 0.0, 0.12, 0.1))
        container_template = 'trash_can/trashcan.urdf'
        trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')
        trashcan_size = p.getVisualShapeData(trashcan_id)[0][3]

        target_place_type=random.choice(["stand2trashcan","primitive","block2trashcan"])

        base_size = (0.06, 0.18, 0.005)
        if target_place_type=="stand2trashcan":
            base_urdf = 'stacking/stand.urdf'
            base_pose = self.get_random_pose(env, base_size)
            base_id=env.add_object(base_urdf, base_pose, 'fixed')

            ## Add adv stand obj
            true_pose = p.getBasePositionAndOrientation(base_id)
            current_pos = utils.determine_region(true_pose,self)
            i = 0
            rel_pos= ['top left', 'top right', 'bottom left', 'bottom right']
            rel_pos.remove(current_pos)
            while i < 20:
                adv_pos = random.choice(rel_pos)
                pose = self.get_random_pose(env, base_size, zone=adv_pos)
                adv_obj_id = env.add_object(base_urdf, pose)

                if adv_obj_id is not None:
                    break
                i += 1
            if adv_obj_id ==None:
                return False

            obj_points = {adv_obj_id: self.get_object_points(trashcan_id)}
            obj_ids = []
            obj_ids.append((adv_obj_id, (0, None)))
            self.goals.append((
                obj_ids, np.eye(1), [trashcan_pose], False, False, 'trash',
                (obj_points, [(trashcan_pose, trashcan_size)]), 1))

            lang_template = "put the stand at the "+adv_pos+" into the trashcan"
            question_template = "Did the robot successfully execute the action 'put the stand at the "+adv_pos+" into the trashcan', and did any anomaly happen?"
            self.lang_goals.append(lang_template)
            self.question_list.append(question_template)

        else:
            # Add base.

            base_urdf = 'stacking/stand.urdf'
            base_pose = self.get_random_pose(env, base_size)
            env.add_object(base_urdf, base_pose, 'fixed')

            # Block colors.
            color_names = self.get_colors()

            # Shuffle the block colors.
            random.shuffle(color_names)
            colors = [utils.COLORS[cn] for cn in color_names]

            # Add blocks.
            objs = []
            # sym = np.pi / 2
            block_urdf = 'stacking/block.urdf'


            # Associate placement locations for goals.
            place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
                         (0, 0.05, 0.03), (0, -0.025, 0.08),
                         (0, 0.025, 0.08), (0, 0, 0.13)]
            targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
            obj_points={trashcan_id:self.get_object_points(trashcan_id)}
            nbr_blocks=random.randint(1,6)

            for i in range(nbr_blocks):
                block_pose = targs[i]
                block_id = env.add_object(block_urdf, block_pose)
                p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
                objs.append((block_id, (np.pi / 2, None)))
            if target_place_type=="block2trashcan":

                adv_info = self.add_adv_objects(env, (0.04, 0.04, 0.04), block_urdf, 2, colors[nbr_blocks])
                if adv_info is None:
                    return None
                valid_block_ids, pick_pos = adv_info
                adv_obj_id = valid_block_ids[-1]
                obj_points = {adv_obj_id: self.get_object_points(trashcan_id)}
                obj_ids = []
                obj_ids.append((adv_obj_id, (0, None)))

                self.goals.append((
                    obj_ids, np.eye(1), [trashcan_pose], False, False, 'trash',
                    (obj_points, [(trashcan_pose, trashcan_size)]), 1))

                lang_template = "put the "+color_names[nbr_blocks]+" block at the " + pick_pos[-1] + " into the trashcan"
                question_template = "Did the robot successfully execute the action "+lang_template +", and did any anomaly happen?"
                self.lang_goals.append(lang_template)
                self.question_list.append(question_template)
                
            else:
                if nbr_blocks==6:
                    # Goal: remove the top row.
                    self.goals.append(([objs[5]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[5] ,
                                                                     position=f"on the {color_names[3]} and {color_names[4]} blocks"))
                    self.question_list.append(self.question_template.format(pick=color_names[5] ,
                                                                     position=f"on the {color_names[3]} and {color_names[4]} blocks"))
                elif nbr_blocks==5:
                    # Goal: remove the middle row.
                    self.goals.append(([objs[4]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[4],
                                                                     position=f"on the {color_names[1]} and {color_names[2]} blocks"))
                    self.question_list.append(self.question_template.format(pick=color_names[4],
                                                                     position=f"on the {color_names[1]} and {color_names[2]} blocks"))
                elif nbr_blocks == 4:
                    self.goals.append(([objs[3]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[3],
                                                                     position=f"on the {color_names[0]} and {color_names[1]} blocks"))
                    self.question_list.append(self.question_template.format(pick=color_names[2],
                                                                     position=f"on the {color_names[0]} and {color_names[1]} blocks"))
                elif nbr_blocks == 3:
                    # Goal: remove  the bottom row.
                    self.goals.append(([objs[2]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[2],
                                                                     position=f"on the darkest brown block of the stand"))
                    self.question_list.append(self.question_template.format(pick=color_names[2],
                                                                     position=f"on the darkest brown block of the stand"))

                elif nbr_blocks == 2:
                    self.goals.append(([objs[1]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[1],
                                                                     position=f"on the middle brown block of the stand"))
                    self.question_list.append(self.lang_template.format(pick=color_names[1],
                                                                     position=f"on the middle brown block of the stand"))
                elif nbr_blocks == 1:
                    self.goals.append(([objs[0]], np.eye(1), [trashcan_pose],
                                       False, False, 'trash', (obj_points, [(trashcan_pose, trashcan_size)]), 1))
                    self.lang_goals.append(self.lang_template.format(pick=color_names[0],
                                                                     position=f"on the lightest brown block of the stand"))
                    self.question_list.append(self.question_template.format(pick=color_names[0],
                                                                     position=f"on the lightest brown block of the stand"))

        self.answer_list.append(self.answer_template)
        return True
    def get_colors(self):
        return utils.ALL_COLORS


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