for h in 8 16 32 64 128 256 512
do
    let b=$h/2
    CUDA_VISIBLE_DEVICES="1" python NeuralFM.py --epoch 120 --batch_size 32 --lr 0.01 --hidden_factor $h --layers [$h,$b] --log_path zhankui --log_on [\'hidden_factor\',\'layers\'];
done