"""Packing Google Objects tasks."""

import os

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils
import random
import pybullet as p



object_names=[
                'alarm clock',
                'android toy',
                'ball puzzle',
                'black and blue sneakers',
                'black boot with leopard print',
                'black fedora',
                'black razer mouse',
                'black sandal',
                'black shoe with green stripes',
                'black shoe with orange stripes',
                'brown fedora',
                'bull figure',
                'butterfinger chocolate',
                'c clamp',
                'can opener',
                'crayon box',
                'dinosaur figure',
                'dog statue',
                'frypan',
                'green and white striped towel',
                'grey soccer shoe with cleats',
                'hammer',
                'hard drive',
                'honey dipper',
                'light brown boot with golden laces',
                'lion figure',
                'magnifying glass',
                'mario figure',
                'nintendo 3ds',
                'nintendo cartridge',
                'orca plush toy',
                'porcelain cup',
                'porcelain salad plate',
                'porcelain spoon',
                'purple tape',
                'red and white flashlight',
                'red and white striped towel',
                'red cup',
                'rhino figure',
                'rocket racoon figure',
                'scissors',
                'screwdriver',
                'silver tape',
                'spatula with purple head',
                'spiderman figure',
                'tablet',
                'toy school bus',
                'toy train',
                'unicorn toy',
                'white razer mouse',
                'yoshi figure']

class PackingGoogleObjectsPrimitive(Task):
    """Packing Google Objects.
    This class will initialize itermediate state of the packing process
    """

    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.task_name="pack-google-object-primitive"
        self.task_completed_desc = "done packing google objects."
        self.answer_template = "The action is executed successfully."
        self.lang_template = "put the {pick_obj} in the brown box"
        self.question_template = "Did the robot successfully execute the action 'put the {pick_obj} in the brown box', and did any anomaly happen?"



    def reset(self, env):
        super().reset(env)

        # target = random.choice(["brown box", "trash can"])

        # add trash can
        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))

        container_template = 'trash_can/trashcan.urdf'
        #trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')



        # object names

        # Add container box.
        zone_size = self.get_random_size(0.2, 0.35, 0.2, 0.35, 0.05, 0.05)
        zone_pose = self.get_random_pose(env, zone_size)
        container_template = 'container/container-template.urdf'
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        container_urdf = self.fill_template(container_template, replace)
        env.add_object(container_urdf, zone_pose, 'fixed')
        if os.path.exists(container_urdf): os.remove(container_urdf)

        margin = 0.01
        min_object_dim = 0.08
        bboxes = []

        # Construct K-D Tree to roughly estimate how many objects can fit inside the box.
        # TODO(Mohit): avoid building K-D Trees
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

        # Add Google Scanned Objects to scene.
        object_points = {}
        object_ids = []
        bboxes = np.array(bboxes)
        scale_factor = 5
        object_template = 'google/object-template.urdf'
        chosen_objs, repeat_category = self.choose_objects(object_names, len(bboxes))
        object_descs = []
        for i, bbox in enumerate(bboxes):
            size = bbox[3:] - bbox[:3]
            max_size = size.max()
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2
            shape_size = max_size * scale_factor
            pose = self.get_random_pose(env, size)

            # Add object only if valid pose found.
            if pose[0] is not None:
                # Initialize with a slightly tilted pose so that the objects aren't always erect.
                slight_tilt = utils.q_mult(pose[1], (-0.1736482, 0, 0, 0.9848078))
                ps = ((pose[0][0], pose[0][1], pose[0][2]+0.05), slight_tilt)

                object_name = chosen_objs[i]
                object_name_with_underscore = object_name.replace(" ", "_")
                mesh_file = os.path.join(self.assets_root,
                                         'google',
                                         'meshes_fixed',
                                         f'{object_name_with_underscore}.obj')
                texture_file = os.path.join(self.assets_root,
                                            'google',
                                            'textures',
                                            f'{object_name_with_underscore}.png')

                try:
                    replace = {'FNAME': (mesh_file,),
                               'SCALE': [shape_size, shape_size, shape_size],
                               'COLOR': (0.2, 0.2, 0.2)}
                    urdf = self.fill_template(object_template, replace)
                    box_id = env.add_object(urdf, ps)
                    if os.path.exists(urdf):
                        os.remove(urdf)
                    object_ids.append((box_id, (0, None)))

                    texture_id = p.loadTexture(texture_file)
                    p.changeVisualShape(box_id, -1, textureUniqueId=texture_id)
                    p.changeVisualShape(box_id, -1, rgbaColor=[1, 1, 1, 1])
                    object_points[box_id] = self.get_object_points(box_id)

                    object_descs.append(object_name)
                except Exception as e:
                    print("Failed to load Google Scanned Object in PyBullet")
                    print(object_name_with_underscore, mesh_file, texture_file)
                    print(f"Exception: {e}")

        ## always pick the fist google obj
        target_obj_id=object_ids[0][0]
        chosen_obj_pts = {target_obj_id: object_points[target_obj_id]}

        self.goals.append(([(target_obj_id, (0, None))], np.int32([[1]]), [zone_pose],
                           False, True, 'zone',
                           (chosen_obj_pts, [(zone_pose, zone_size)]),
                           1))
        self.lang_goals.append(self.lang_template.format(pick_obj=object_descs[0]))
        self.question_list.append(self.question_template.format(pick_obj=object_descs[0]))
        self.answer_list.append(self.answer_template)



        for i in range(480):
            p.stepSimulation()

        return True

    def choose_objects(self, object_names, k):
        repeat_category = None
        return np.random.choice(object_names, k, replace=False), repeat_category
rel_postion = ['top left', 'top right', 'bottom left', 'bottom right']

class PackingGoogleObjectsRelativePrimitive(Task):
    """Packing Google Objects with position difference.
    """
    def __init__(self):
        super().__init__()
        self.max_steps = 1
        self.task_name="pack-google-object-primitive"
        self.task_completed_desc = "done packing google objects."
        self.answer_template = "The action is executed successfully."
        self.lang_template = "put the {pick_obj} at the {pick_pos} in the trashcan"
        self.question_template = "Did the robot successfully execute the action 'put the {pick_obj} at the {pick_pos} in the trashcan', and did any anomaly happen?"
        #self.rel_pos=rel_postion

    def reset(self, env):
        super().reset(env)

        target = random.choice(["obj", "box"])

        # add trash can
        trashcan_pose = ((0.35, random.choice([-0.4, 0.4]), 0.05), (0.0, 0.0, 0.12, 0.1))

        container_template = 'trash_can/trashcan.urdf'
        trashcan_id=env.add_object(container_template, trashcan_pose, 'fixed')
        trashcan_size = p.getVisualShapeData(trashcan_id)[0][3]

        # Add container box.
        zone_size = self.get_random_size(0.2, 0.35, 0.2, 0.35, 0.05, 0.05)
        zone_pose = self.get_random_pose(env, zone_size)
        container_template = 'container/container-template.urdf'
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        container_urdf = self.fill_template(container_template, replace)
        container_id=env.add_object(container_urdf, zone_pose, 'fixed')
        if os.path.exists(container_urdf): os.remove(container_urdf)

        margin = 0.01
        min_object_dim = 0.08
        bboxes = []

        # Construct K-D Tree to roughly estimate how many objects can fit inside the box.
        # TODO(Mohit): avoid building K-D Trees
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

        # Add Google Scanned Objects to scene.
        object_points = {}
        object_ids = []
        bboxes = np.array(bboxes)
        scale_factor = 5
        object_template = 'google/object-template.urdf'
        chosen_objs, repeat_category = self.choose_objects(object_names, len(bboxes))
        object_descs = []
        adv_step=2
        adv_id=None
        for i, bbox in enumerate(bboxes):
            size = bbox[3:] - bbox[:3]
            max_size = size.max()
            position = size / 2. + bbox[:3]
            position[0] += -zone_size[0] / 2
            position[1] += -zone_size[1] / 2
            shape_size = max_size * scale_factor
            pose = self.get_random_pose(env, size)

            # Add object only if valid pose found.
            if pose[0] is not None:
                # Initialize with a slightly tilted pose so that the objects aren't always erect.
                slight_tilt = utils.q_mult(pose[1], (-0.1736482, 0, 0, 0.9848078))
                ps = ((pose[0][0], pose[0][1], pose[0][2]+0.05), slight_tilt)

                object_name = chosen_objs[i]
                object_name_with_underscore = object_name.replace(" ", "_")
                mesh_file = os.path.join(self.assets_root,
                                         'google',
                                         'meshes_fixed',
                                         f'{object_name_with_underscore}.obj')
                texture_file = os.path.join(self.assets_root,
                                            'google',
                                            'textures',
                                            f'{object_name_with_underscore}.png')

                try:
                    replace = {'FNAME': (mesh_file,),
                               'SCALE': [shape_size, shape_size, shape_size],
                               'COLOR': (0.2, 0.2, 0.2)}
                    urdf = self.fill_template(object_template, replace)
                    box_id = env.add_object(urdf, ps)
                    #print(target)
                    if (target=="obj") and (i==adv_step):
                        adv_info=self.add_adv_google_object(box_id,urdf,size,env)
                        #print("fuck")
                        #print(adv_info)
                        if adv_info is None:
                            return None
                        pick_obj_name=object_descs[0]
                        adv_id, adv_pos = adv_info
                        texture_id = p.loadTexture(texture_file)
                        p.changeVisualShape(adv_id, -1, textureUniqueId=texture_id)
                        p.changeVisualShape(adv_id, -1, rgbaColor=[1, 1, 1, 1])


                    object_ids.append((box_id, (0, None)))

                    texture_id = p.loadTexture(texture_file)
                    p.changeVisualShape(box_id, -1, textureUniqueId=texture_id)
                    p.changeVisualShape(box_id, -1, rgbaColor=[1, 1, 1, 1])
                    object_points[box_id] = self.get_object_points(box_id)

                    object_descs.append(object_name)
                    if os.path.exists(urdf):
                        os.remove(urdf)
                except Exception as e:
                    print("Failed to load Google Scanned Object in PyBullet")
                    print(object_name_with_underscore, mesh_file, texture_file)
                    print(f"Exception: {e}")
                    return None


        #print(target)
        ## always pick the fist google obj
        if target=="box":
            zone_size = self.get_random_size(0.05, 0.1, 0.05, 0.1, 0.05, 0.05)
            half = np.float32(zone_size) / 2
            replace = {'DIM': zone_size, 'HALF': half}
            container_urdf = self.fill_template(container_template, replace)
            adv_info = self.add_adv_google_object(container_id, container_urdf, zone_size, env)
            if adv_info is None:
                return None
            adv_id, adv_pos = adv_info
            pick_obj_name = "brown box"
        if adv_id==None:
            return None
        chosen_obj_pts = {adv_id: self.get_object_points(adv_id)}




        self.goals.append(([(adv_id, (0, None))], np.int32([[1]]), [trashcan_pose],
                           False, False, 'trash',
                           (chosen_obj_pts, [(trashcan_pose, trashcan_size)]),
                           1))
        self.lang_goals.append(self.lang_template.format(pick_obj=pick_obj_name,pick_pos=adv_pos))
        self.question_list.append(self.question_template.format(pick_obj=pick_obj_name,pick_pos=adv_pos))
        self.answer_list.append(self.answer_template)



        for i in range(480):
            p.stepSimulation()

        return True

    def choose_objects(self, object_names, k):
        repeat_category = None
        return np.random.choice(object_names, k, replace=False), repeat_category

    def add_adv_google_object(self,obj_id, urdf,object_size,env):

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
                print(adv_pos)
                return adv_obj_id, adv_pos
            i+=1
        return None