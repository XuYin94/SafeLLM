
#  for action_error in True False; do
#  for add_anomaly in True False; do
#     python cliport/anomaly_generator_pack_boxes.py  task=pack-box-anomaly n=500 data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/vlm add_action_error=$action_error add_anomaly=$add_anomaly

#  done
#  done


for action_error in True False; do
 for add_anomaly in True False; do

    python cliport/anomaly_generator_block_bowl.py  task=put-block-in-matching-bowl n=2000 data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/vlm add_action_error=$action_error add_anomaly=$add_anomaly

 done
 done

#  for action_error in True False; do
#  for add_anomaly in True False; do

#     python cliport/anomaly_generator_stack_pyramid.py  task=stack-block-pyramid-seq-unseen-colors n=2000 data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/vlm add_action_error=$action_error add_anomaly=$add_anomaly

#  done
#  done