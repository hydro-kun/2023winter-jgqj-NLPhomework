import os
from File_Path import *

MODEL_NAME = 'TransE_l2'
BATCH_SIZE = 1000
NEG_SAMPLE_SIZE = 200
HIDDEN_DIM = 400
GAMMA = 19.9
LR = 0.25
MAX_STEP = 5000
LOG_INTERVAL = 100
BATCH_SIZE_EVAL = 16
REGULARIZATION_COEF = 1.00E-09
NUM_THREAD = 1
NUM_PROC = 8

# 将'genre_to_movie.json' 'actors_to_movie.json' 'writer_to_movie.json'
# 三个文件放到Data/KGE_Data/下，然后运行Do_KGE即可，
# 将自动提取json文件的三元组并进行训练，
# 日志文件写到KGE_Log_Path，嵌入文件写到KGE_Save_Path

def Do_KGE(model_name = MODEL_NAME,data_path=KGE_Data_path,save_path=KGE_Save_Path,
           batch_size=BATCH_SIZE,neg_sample_size=NEG_SAMPLE_SIZE,hidden_dim=HIDDEN_DIM,
           gamma=GAMMA,lr=LR,max_step=MAX_STEP,log_interval=LOG_INTERVAL,
           batch_size_eval=BATCH_SIZE_EVAL,regularization_coef=REGULARIZATION_COEF,
           num_thread=NUM_THREAD,num_proc=NUM_PROC,log_path=KGE_Log_Path):
    
    # os.popen('nohup sleep 100 | echo "done!" > nohup.log &')
    command = "nohup dglke_train --model_name {model_name}  --dataset movie --data_path {data_path} --save_path {save_path} --format raw_udd_hrt --data_files train.txt valid.txt test.txt --batch_size {batch_size} --neg_sample_size {neg_sample_size} --hidden_dim {hidden_dim} --gamma {gamma} --lr {lr} --max_step {max_step} --log_interval {log_interval} --batch_size_eval {batch_size_eval} -adv --regularization_coef {regularization_coef} --test --num_thread {num_thread} --gpu 0 >> {log_path} &".format(
            model_name =model_name,data_path=data_path,save_path=save_path,
           batch_size=batch_size,neg_sample_size=neg_sample_size,hidden_dim=hidden_dim,
           gamma=gamma,lr=lr,max_step=max_step,log_interval=log_interval,
           batch_size_eval=batch_size_eval,regularization_coef=regularization_coef,
           num_thread=num_thread,num_proc=num_proc,log_path=log_path)
    #print(command)
    os.system('python3 {com} > {log_path}'.format(com=Read_Json_Path,log_path=log_path))
    os.system(command)
    #print(a)

if __name__ == '__main__':
    Do_KGE()