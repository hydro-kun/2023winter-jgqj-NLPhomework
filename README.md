# 复现报告代码部分说明

## 复现结果说明

### UMGF

`./UMGF/UMGF_OUTPUT`下为UMGF训练和测试的结果输出，其中`twitter2015`和`twitter2017`为UMGF在数据集twitter2017和twitter2015上的复现结果，`twitter2015_best_ckpt`和`twitter2017_best_ckpt`为测试作者提供的`model.pt`的测试结果

`UMGF_TEST_OUT.txt`和`UMGF_TRAIN_OUT.txt`分别为测试输出文件和训练输出文件，
`UMGF_TEST_OUT_60epoch.txt`和`UMGF_TRAIN_OUT_epoch.txt`分别为训练60个epoch的测试输出文件和训练输出文件，
其中`UMGF_TEST_OUT.txt`的输出格式如下：
```bash
overall             accuracy,   precision,  recall,     F1
PER(PERSON)         precision,  recall,     F1
LOC(LOCATION)       precision,  recall,     F1
ORG(ORGANIZATION)   precision,  recall,     F1
OTHER(OTHER)        precision,  recall,     F1
```

### UMT

`./UMT/UMT_OUTPUT`下为UMT训练和测试的结果输出，其中

`UMT_OUT_2015.txt`和`UMT_OUT_2017.txt`为UMGT在数据集twitter2015和twitter2017上训练，在不同的数据集上测试的测试结果；

`UMT_OUT_2015_same.txt`和`UMT_OUT_2017_same.txt`为UMGT在数据集twitter2015和twitter2017上训练，在相同的数据集上测试的测试结果

## 复现代码说明

从[UMGF-github](https://github.com/TransformersWsz/UMGF)和[UMT-github](https://github.com/jefferyYu/UMT)下载代码，可能会遇到的问题可以参考[复现过程和遇到的问题](https://www.wolai.com/vitbcxTewBQ6sdiT3qiPp3)

将UMGF和UMT文件夹按照目录结构放到下载的文件夹中，并替换对应的文件

### 数据集

Twitter2015和twitter2017数据集的文本部分已提供，图片从[GoogleDrive](https://drive.google.com/file/d/1PpvvncnQkgDNeBMKVgG2zFYuRhbL873g/view)下载；

对于UMGF，则需要按照[One-Stage Visual Grounding](https://github.com/TransformersWsz/onestage_grounding/blob/master/README.md)的方法为每个单词在图中检测对应的视觉对象，并画出边界框，并将图片放在./data/twitter2015/image下。
(或直接从[twitter2015_img.tar.gz(password: l75t)](https://pan.baidu.com/s/1DCACHmDKYiW21Vnmn6YIvQ?pwd=l75t) 和[twitter2017_img.tar.gz(password: 2017)](https://pan.baidu.com/s/173PbLBFWDEHjWH3zLtzZww?pwd=2017)下载)

## 运行测试

```bash
# 运行UMGF的训练和测试，输出文件在my_code下
cd UMGF/my_code
./train_twitter.sh

# 运行UMT的训练和测试，输出文件在UMT下
cd UMT
./run_test.sh
```
