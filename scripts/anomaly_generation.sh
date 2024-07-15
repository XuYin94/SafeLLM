# for action_error in True False; do
# for add_anomaly in True False; do

#    python cliport/anomaly_generator_block_bowl.py  task=put-block-in-matching-bowl  n=1000 data_dir=/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm add_action_error=$action_error add_anomaly=$add_anomaly

# done

# done
 for action_error in True False; do
 for add_anomaly in True False; do

    python cliport/anomaly_generator_pack_boxes.py  task=pack-box-primitive n=10 data_dir=/mnt/lynx4/users/zhang/yinxu/Workfolder/data/vlm add_action_error=$action_error add_anomaly=$add_anomaly

 done
 done