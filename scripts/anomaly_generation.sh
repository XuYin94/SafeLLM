 #python cliport/episode_generator.py  n=100 
 for TASK_NAME in put-block-in-matching-bowl

 do

    python cliport/anomaly_generator_block_bowl.py  task=$TASK_NAME  n=10000 data_dir=/mnt/lynx1/users/zhang/Workfolder/data/vlm/anomaly/  episode_data_dir=/mnt/lynx1/users/zhang/Workfolder/data/episodes/

 done

# for TASK_NAME in pack-box-primitive

# do

#    python cliport/anomaly_generator_pack_boxes.py  task=$TASK_NAME  n=10000 data_dir=/mnt/lynx1/users/zhang/Workfolder/data/vlm/anomaly/

# done