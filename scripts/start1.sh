#!/bin/bash

#DATA_DIR=$1
DISP=False

echo "Generating dataset... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

LANG_TASKS='stack-block-pyramid-seq-seen-colors-primitive stack-block-pyramid-seq-seen-colors-relative-position'
for task in $LANG_TASKS
    do
        python cliport/primitive_generator.py task=$task mode=train n=1000 data_dir=/mnt/nas4/yinxu/LLM_workspace/primitive/new disp=$DISP &
        python cliport/primitive_generator.py task=$task mode=val   n=100 data_dir=/mnt/nas4/yinxu/LLM_workspace/primitive/new disp=$DISP &
    done
echo "Finished Language Tasks."


