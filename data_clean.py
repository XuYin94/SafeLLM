import os 
import shutil

# def change_name(path):
#     for i,file_name in enumerate(os.listdir(path)):
#         idx, seed=file_name.split('-')
#         new=f'{i:06d}-{seed}'
#         old_file=os.path.join(path,file_name)
#         new_file=os.path.join(path,new)
#         #print(new_file)
#         os.rename(old_file,new_file)

# for type in ['action','color','depth','reward','font_img','topdown_img','info']:
#     change_name("/mnt/nas2/yinxu/Worker_folder/loranvens/data/pack-box-primitive-train/"+type+"")


#import os

# def get_filenames_in_folder(folder):
#     filenames = set()
#     for root, dirs, files in os.listdir(folder):
#         for file in files:
#             filenames.add(file)
#     return filenames

# def compare_folders(folder1, folder2):
#     filenames1 = get_filenames_in_folder(folder1)
#     filenames2 = get_filenames_in_folder(folder2)

#     common_filenames = filenames1.intersection(filenames2)
#     unique_filenames1 = filenames1 - filenames2
#     unique_filenames2 = filenames2 - filenames1

#     return common_filenames, unique_filenames1, unique_filenames2

# # 指定两个文件夹的路径
# folder1_path = '/mnt/nas2/yinxu/Worker_folder/loranvens/data/pack-box-primitive-relative-pick-position-train/topdown_img'
# folder2_path = '/mnt/nas2/yinxu/Worker_folder/loranvens/data/pack-box-primitive-relative-pick-position-train/font_img'

# common_files, unique_files_in_folder1, unique_files_in_folder2 = compare_folders(folder1_path, folder2_path)

# print("共同的文件名:")
# print(len(common_files))
# # for filename in common_files:
# #     print(filename)

# print("\n只存在于文件夹1中的文件名:")
# for filename in unique_files_in_folder1:
#     print(filename)

# print("\n只存在于文件夹2中的文件名:")
# for filename in unique_files_in_folder2:
#     print(filename)
#     #os.remove(os.path.join(folder2_path,filename))
#     #shutil.rmtree(os.path.join(folder2_path,filename))