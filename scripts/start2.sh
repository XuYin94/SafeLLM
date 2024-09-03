
#source /root/miniconda3/etc/profile.d/conda.sh
#conda env list
#source activate loravens

# python setup.py develop
#wandb login 64b0361e494a7e48cf9aab82f6ecd77888550de4
#pick-and-place-primitive pack-box-primitive-relative-pick-position stack-block-pyramid-seq-seen-colors-relative-position
for TASK_NAME in stack-block-pyramid-seq-seen-colors-relative-position
do

    python cliport/primitive_generator.py  task=$TASK_NAME  n=3000 mode=train data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/primitive

    python cliport/primitive_generator.py  task=$TASK_NAME  n=300 mode=val data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/primitive

 done

# python cliport/episode_generator.py n=5000 data_dir=/mnt/lynx4/users/zhang/yinxu/Workfolder/data/


#torchrun --nnodes=1 --master-port 3637 --nproc_per_node=1 open_flamingo/train/fine_tune_test.py --batch_size_robot 8  --num_epochs 10   --warmup_steps  1875  --resume_from_checkpoint /mnt/lynx1/users/zhang/Workfolder/exp/vlm_exp/openflamingo3B/checkpoint_6.pt