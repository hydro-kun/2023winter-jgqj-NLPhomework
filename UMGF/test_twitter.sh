#!/bin/bash
# ./test_twitter.sh 

# echo 'train on twitter2017, test on twitter2017' >> ./twitter2017_UMGF_TEST_OUT_60epoch.txt
# nohup srun -w gn80 python -u ./ddp_mmner.py --do_test --txtdir=./my_data/twitter2017 --imgdir=./data/twitter2017/image --ckpt_path=./model_twitter2017.pt --test_batch_size=32 | col -b >> ./twitter2017_UMGF_TEST_OUT_60epoch.txt
# echo 'train on twitter2017, test on twitter2015' >> ./twitter2017_UMGF_TEST_OUT.txt
# nohup srun -w gn80 python -u ./ddp_mmner.py --do_test --txtdir=./my_data/twitter2015 --imgdir=./data/twitter2015/image --ckpt_path=./model_twitter2017.pt --test_batch_size=32 | col -b >> ./twitter2017_UMGF_TEST_OUT_60epoch.txt

echo 'train on twitter2015, test on twitter2015' >> ./twitter2017_UMGF_TEST_OUT_60epoch.txt
nohup srun -w gn81 python -u ./ddp_mmner.py --do_test --txtdir=./my_data/twitter2015 --imgdir=./data/twitter2015/image --ckpt_path=./model_twitter2015.pt --test_batch_size=32 | col -b >> ./twitter2015_UMGF_TEST_OUT_60epoch.txt
echo 'train on twitter2015, test on twitter2017' >> ./twitter2015_UMGF_TEST_OUT.txt
nohup srun -w gn81 python -u ./ddp_mmner.py --do_test --txtdir=./my_data/twitter2017 --imgdir=./data/twitter2017/image --ckpt_path=./model_twitter2015.pt --test_batch_size=32 | col -b >> ./twitter2015_UMGF_TEST_OUT_60epoch.txt
