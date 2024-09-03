
#source /root/miniconda3/etc/profile.d/conda.sh
#conda env list
#source activate loravens

# python setup.py develop
#wandb login 64b0361e494a7e48cf9aab82f6ecd77888550de4
#pick-and-place-primitive pack-box-primitive-relative-pick-position stack-block-pyramid-seq-seen-colors-relative-position
for TASK_NAME in pack-box-primitive-relative-pick-position
do

    python cliport/primitive_generator.py  task=$TASK_NAME  n=3000 mode=train data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/primitive

    python cliport/primitive_generator.py  task=$TASK_NAME  n=300 mode=val data_dir=/mnt/bear1/users/zhangkang/yinxu/Workfolder/data/primitive

 done

# python cliport/episode_generator.py n=5000 data_dir=/mnt/lynx4/users/zhang/yinxu/Workfolder/data/
