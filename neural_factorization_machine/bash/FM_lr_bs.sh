for lr in 0.001 0.005 0.01 0.05 0.1 0.5
do
    for bs in 32 64
    do
        CUDA_VISIBLE_DEVICES="-1" python FM.py --lr $lr --batch_size $bs --log_path zhankui --log_on [\'lr\',\'batch_size\'];
    done
done