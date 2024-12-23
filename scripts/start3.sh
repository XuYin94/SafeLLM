#!/bin/bash

#DATA_DIR=$1
DISP=False

echo "Generating dataset... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

LANG_TASKS='pack-box-primitive pack-box-primitive-relative-pick-position'
for task in $LANG_TASKS
    do
        python cliport/primitive_generator.py task=$task mode=train  n=1000 data_dir=/mnt/nas4/yinxu/LLM_workspace/primitive/new disp=$DISP &
        python cliport/primitive_generator.py task=$task mode=val   n=100 data_dir=/mnt/nas4/yinxu/LLM_workspace/primitive/new disp=$DISP &
    done
echo "Finished Language Tasks."





# python cliport/episode_generator.py n=5000 data_dir=/mnt/lynx4/users/zhang/yinxu/Workfolder/data/


#torchrun --nnodes=1 --master-port 3637 --nproc_per_node=1 train/fine_tune_test.py --batch_size_robot 12  --num_epochs 10 --warmup_steps 2500 --resume /mnt/bear1/users/zhangkang/yinxu/LLM_models/OpenFlamingo-3B-vitl-mpt1b/base_weight.pt --workers=4