for h in 8 16 32 64 128 256 512
do
    let b=$h/2
    let c=$b/2
    CUDA_VISIBLE_DEVICES="1" python NeuralFM.py --epoch 120 --batch_size 32 --lr 0.01 --hidden_factor $h --layers [$h,$b,$c] --log_path zhankui --keep_prob [0.8,0.5,0.5] --log_on [\'hidden_factor\',\'layers\'];
done