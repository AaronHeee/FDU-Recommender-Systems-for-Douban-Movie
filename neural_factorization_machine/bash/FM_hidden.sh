for h in 8 16 32 64 128 256 512
do
    CUDA_VISIBLE_DEVICES="0" python FM.py --epoch 120 --batch_size 32 --lr 0.005 --hidden_factor $h --log_path zhankui --log_on [\'hidden_factor\'];
done