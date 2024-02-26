#!/bin/bash
# sh ./train_twitter.sh 

python -u ../ddp_mmner.py --do_train --txtdir=../my_data/twitter2015 --imgdir=../data/twitter2015/image --ckpt_path=./model_twitter2015.pt --num_train_epoch=30 --train_batch_size=4 --lr=0.0001 --seed=2019 >> ./twitter2015_UMGF_TRAIN_OUT.txt

python -u ../ddp_mmner.py --do_train --txtdir=../my_data/twitter2017 --imgdir=../data/twitter2017/image --ckpt_path=./model_twitter2017.pt --num_train_epoch=30 --train_batch_size=4 --lr=0.0001 --seed=2019 >> ./twitter2017_UMGF_TRAIN_OUT.txt

sh ./test_twitter.sh 