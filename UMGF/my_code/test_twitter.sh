#!/bin/bash
# ./test_twitter.sh 

echo 'train on twitter2017, test on twitter2017' >> ./twitter2015_UMGF_TRAIN_OUT.txt
python -u ../ddp_mmner.py --do_test --txtdir=../my_data/twitter2017 --imgdir=../data/twitter2017/image --ckpt_path=./model_twitter2017.pt --test_batch_size=4 >> ./twitter2017_UMGF_TRAIN_OUT.txt
echo 'train on twitter2017, test on twitter2015' >> ./twitter2015_UMGF_TRAIN_OUT.txt
python -u ../ddp_mmner.py --do_test --txtdir=../my_data/twitter2015 --imgdir=../data/twitter2015/image --ckpt_path=./model_twitter2017.pt --test_batch_size=4 >> ./twitter2017_UMGF_TRAIN_OUT.txt

echo 'train on twitter2015, test on twitter2015' >> ./twitter2015_UMGF_TRAIN_OUT.txt
python -u ../ddp_mmner.py --do_test --txtdir=../my_data/twitter2015 --imgdir=../data/twitter2015/image --ckpt_path=./model_twitter2015.pt --test_batch_size=4 >> ./twitter2015_UMGF_TRAIN_OUT.txt
echo 'train on twitter2015, test on twitter2017' >> ./twitter2015_UMGF_TRAIN_OUT.txt
python -u ../ddp_mmner.py --do_test --txtdir=../my_data/twitter2017 --imgdir=../data/twitter2017/image --ckpt_path=./model_twitter2015.pt --test_batch_size=4 >> ./twitter2015_UMGF_TRAIN_OUT.txt
