#!/bin/sh

echo ${i}'\n' > out.log

for i in 'UMT_OUT_2017.txt' 'UMT_OUT_2017_same.txt' 'UMT_OUT_2015.txt' 'UMT_OUT_2015_same.txt'
do
    echo ${i}'\n' >> out.log
    cat ${i} | tail -30 >> out.log
done