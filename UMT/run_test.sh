#!/usr/bin/env bash
# ./run_test.sh

nohup srun -w gn80 sh run_2015.sh | col -b >> UMT_OUT_2015.txt &
nohup srun -w gn81 sh run_2015_same.sh | col -b >> UMT_OUT_2015_same.txt &
nohup srun -w gn82 sh run_2017.sh | col -b >> UMT_OUT_2017.txt &
nohup srun -w gn83 sh run_2017_same.sh | col -b >> UMT_OUT_2017_same.txt &

# nohup srun -w gn68 sh test.sh | col -b >> nohup.log &
