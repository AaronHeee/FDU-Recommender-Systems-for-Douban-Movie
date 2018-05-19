for lr in 0.005 0.01 0.05 0.1 0.5
do
    for bs in 16 32 64 128 256 512
    do
        CUDA_VISIBLE_DEVICES="-1" python NeuralFM.py --lr $lr --batch_size $bs --log_path zhankui --log_on [\'lr\',\'batch_size\'];
    done
done