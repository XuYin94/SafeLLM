 for TASK_NAME in pick-and-place-primitive pack-box-primitive

 do

    python cliport/primitive_anomaly_generator.py  task=$TASK_NAME  n=10000 data_dir=/mnt/lynx1/users/zhang/Workfolder/data/vlm/anomaly/

 done