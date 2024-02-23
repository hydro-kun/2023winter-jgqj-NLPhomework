'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-16 21:33:11
LastEditors: Ga1axy_z
LastEditTime: 2023-04-20 18:41:51
'''
import json
import random
import pymysql

import os
import sys                                                                      # 实现在文件夹内部的 Python 文件中应用文件夹外部的 Python 文件，这里既 py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))     # 获取父级目录的路径
sys.path.append(parent_dir)                                                     # 将父级目录的路径添加到 sys.path 中
from File_Path import *

# 查询数据库，获取所有的电影类型名称
def get_genre_info() :
    db = pymysql.connect(host='localhost',  # 打开数据库连接
                        user='root',
                        password='root',
                        database='douban_movies')
    cursor = db.cursor()                    # 使用 cursor() 方法创建一个游标对象 cursor
    sql = "SELECT * FROM Genre_Info;"
    try:
        cursor.execute(sql)                 # 执行SQL语句
        results = cursor.fetchall()         # 获取所有记录列表,以元组来存储
    except Exception as e:
        print(repr(e))
    cursor.close()                          # 关闭不使用的游标对象
    db.close()                              # 关闭数据库连接
    return results

# 获取名称并保存到文件中，五个实体各自的数据集用来构造 AC 树，所有演职人员和电影的名称用来构造训练朴素贝叶斯分类器模型所需的数据集
def get_name() :

    # 获取全部的电影名称
    with open(doubanID_Path,'r',encoding='utf-8') as f:
        All_Movies_Pro_Info = json.load(f)
    All_Movies_Name_Pro = open(All_Movies_Name_Pro_Path,'w',encoding='utf-8')
    for item in All_Movies_Pro_Info :
        All_Movies_Name_Pro.write(item["title"] + '\n')

    # 获取【已爬取的演职人员】名称，包括导演、编剧、主演
    with open(All_Celebrities_Info_Temp_Path,'r',encoding='utf-8') as f:
        All_Celebrities_Info = json.load(f)
    All_Celebrities_Name = open(All_Celebrities_Name_Path,'w',encoding='utf-8')
    for item in All_Celebrities_Info :
        if item["Ch_Name"] != "" :
            All_Celebrities_Name.write(item["Ch_Name"] + '\n')

    # 获取已爬取的电影类型名称
    All_Genres_Info = get_genre_info()
    All_Genres_Name = open(All_Genres_Name_Path,'w',encoding='utf-8')
    for item in All_Genres_Info :
        All_Genres_Name.write(item[1] + '\n')

    # 获取已爬取的电影名称
    with open(All_Movies_Info_Temp_Path,'r',encoding='utf-8') as f:
        All_Movies_Info = json.load(f)
    All_Movies_Name = open(All_Movies_Name_Path,'w',encoding='utf-8')
    for item in All_Movies_Info :
        All_Movies_Name.write(item["Name"] + '\n')

    # 获取【已爬取的电影】相关的导演名称，实际上数据库中爬取到的人员信息没有这么多（没爬完）
    All_Directors_Name = open(All_Directors_Name_Path,'w',encoding='utf-8')
    for item in All_Movies_Info :
        if item["Director"][1] != "" :
            All_Directors_Name.write(item["Director"][1] + '\n')

    # 获取【已爬取的电影】相关的编剧名称，实际上数据库中爬取到的人员信息没有这么多（没爬完）
    All_Writers_Name = open(All_Writers_Name_Path,'w',encoding='utf-8')
    for item in All_Movies_Info :
        for each in item["Writer"] :
            if each[1] != "" :
                All_Writers_Name.write(each[1] + '\n')
    
    # 获取【已爬取的电影】相关的主演名称，实际上数据库中爬取到的人员信息没有这么多（没爬完）
    All_Actors_Name = open(All_Actors_Name_Path,'w',encoding='utf-8')
    for item in All_Movies_Info :
        for each in item["Actors"] :
            if each[1] != "" :
                All_Actors_Name.write(each[1] + '\n')
    
# 读取文件中的每一行，组成一个列表
def read_words(file_path) :
    with open(file_path, 'r', encoding='utf-8') as f :
        words = [line.strip() for line in f]
    return words

# 生成关于【电影】的问句
def build_movie_question(Question_Training_Dataset) :
    
    All_Movies_Name = read_words(All_Movies_Name_Path)                # 读取问句的对象
    random.shuffle(All_Movies_Name)                                   # 随机打乱名称的顺序

    # 读取问句的主体
    QT_Movie_Another_Name = read_words(QT_Movie_Another_Name_Path)
    QT_Movie_Poster = read_words(QT_Movie_Poster_Path)
    QT_Movie_Duration = read_words(QT_Movie_Duration_Path)
    QT_Movie_Release_Date = read_words(QT_Movie_Release_Date_Path)
    QT_Movie_Rating = read_words(QT_Movie_Rating_Path)
    QT_Movie_Language = read_words(QT_Movie_Language_Path)
    QT_Movie_Summary = read_words(QT_Movie_Summary_Path)
    QT_Movie_Director = read_words(QT_Movie_Director_Path)
    QT_Movie_Writer = read_words(QT_Movie_Writer_Path)
    QT_Movie_Actors = read_words(QT_Movie_Actors_Path)
    QT_Movie_Genre = read_words(QT_Movie_Genre_Path)

    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Movies_Name)):
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Another_Name[i % len(QT_Movie_Another_Name)] + ",电影别名"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Poster[i % len(QT_Movie_Poster)] + ",电影海报"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Duration[i % len(QT_Movie_Duration)] + ",电影时长"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Release_Date[i % len(QT_Movie_Release_Date)] + ",电影上映时间"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Rating[i % len(QT_Movie_Rating)] + ",电影豆瓣评分"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Language[i % len(QT_Movie_Language)] + ",电影涉及的语言"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Summary[i % len(QT_Movie_Summary)] + ",电影剧情简介"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Director[i % len(QT_Movie_Director)] + ",电影的导演"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Writer[i % len(QT_Movie_Writer)] + ",电影的编剧"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Actors[i % len(QT_Movie_Actors)] + ",电影的主演"
        Question_Training_Dataset.write(combined + '\n')
        combined = "《" + All_Movies_Name[i] + "》" + QT_Movie_Genre[i % len(QT_Movie_Genre)] + ",电影的类型"
        Question_Training_Dataset.write(combined + '\n')

# 生成关于【演职人员】的问句
def build_celebrity_question(Question_Training_Dataset) :
    
    All_Celebrity_Name = read_words(All_Celebrities_Name_Path)        # 读取问句的对象
    random.shuffle(All_Celebrity_Name)                                          # 随机打乱名称的顺序

    # 读取问句的主体
    QT_Celebrity_Eng_Name = read_words(QT_Celebrity_Eng_Name_Path)
    QT_Celebrity_Gender = read_words(QT_Celebrity_Gender_Path)
    QT_Celebrity_Constellation = read_words(QT_Celebrity_Constellation_Path)
    QT_Celebrity_Poster = read_words(QT_Celebrity_Poster_Path)
    QT_Celebrity_Birthday = read_words(QT_Celebrity_Birthday_Path)
    QT_Celebrity_Birthplace = read_words(QT_Celebrity_Birthplace_Path)
    QT_Celebrity_Occupation = read_words(QT_Celebrity_Occupation_Path)
    QT_Celebrity_Description = read_words(QT_Celebrity_Description_Path)
    
    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Celebrity_Name)):
        combined = All_Celebrity_Name[i] + QT_Celebrity_Eng_Name[i % len(QT_Celebrity_Eng_Name)] + ",外文名"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Gender[i % len(QT_Celebrity_Gender)] + ",性别"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Constellation[i % len(QT_Celebrity_Constellation)] + ",星座"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Poster[i % len(QT_Celebrity_Poster)] + ",海报"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Birthday[i % len(QT_Celebrity_Birthday)] + ",生日"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Birthplace[i % len(QT_Celebrity_Birthplace)] + ",出生地"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Occupation[i % len(QT_Celebrity_Occupation)] + ",所有职业"
        Question_Training_Dataset.write(combined + '\n')
        combined = All_Celebrity_Name[i] + QT_Celebrity_Description[i % len(QT_Celebrity_Description)] + ",个人简介"
        Question_Training_Dataset.write(combined + '\n')

# 生成关于【电影类型】的问句
def build_type_question(Question_Training_Dataset) :
    
    All_Genres_Name = read_words(All_Genres_Name_Path)                # 读取问句的对象
    random.shuffle(All_Genres_Name)                                             # 随机打乱名称的顺序
    QT_Genre_Movie = read_words(QT_Genre_Movie_Path)                  # 读取问句的主体
    
    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Genres_Name)):
        combined = All_Genres_Name[i] + QT_Genre_Movie[i % len(QT_Genre_Movie)] + ",类型包括的电影"
        Question_Training_Dataset.write(combined + '\n')

# 生成关于【导演】的补充问句
def build_director_question(Question_Training_Dataset) :
    
    All_Directors_Name = read_words(All_Directors_Name_Path)          # 读取问句的对象
    random.shuffle(All_Directors_Name)                                          # 随机打乱名称的顺序
    QT_Director_Directed = read_words(QT_Director_Directed_Path)      # 读取问句的主体
    
    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Directors_Name)):
        combined = All_Directors_Name[i] + QT_Director_Directed[i % len(QT_Director_Directed)] + ",导演执导的电影"
        Question_Training_Dataset.write(combined + '\n')

# 生成关于【编剧】的补充问句
def build_writer_question(Question_Training_Dataset) :
    
    All_Writers_Name = read_words(All_Writers_Name_Path)              # 读取问句的对象
    random.shuffle(All_Writers_Name)                                            # 随机打乱名称的顺序
    QT_Writer_Written = read_words(QT_Writer_Written_Path)            # 读取问句的主体
    
    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Writers_Name)):
        combined = All_Writers_Name[i] + QT_Writer_Written[i % len(QT_Writer_Written)] + ",编剧编写的电影"
        Question_Training_Dataset.write(combined + '\n')

# 生成关于【主演】的补充问句
def build_actors_question(Question_Training_Dataset) :
    
    All_Actors_Name = read_words(All_Actors_Name_Path)                # 读取问句的对象
    random.shuffle(All_Actors_Name)                                             # 随机打乱名称的顺序
    QT_Actors_Starred = read_words(QT_Actors_Starred_Path)            # 读取问句的主体
    
    # 将问句的对象和问句的主体随机组合
    for i in range(len(All_Actors_Name)):
        combined = All_Actors_Name[i] + QT_Actors_Starred[i % len(QT_Actors_Starred)] + ",演员主演的电影"
        Question_Training_Dataset.write(combined + '\n')


def build_question() :
    Question_Training_Dataset = open(Question_Training_Dataset,'w',encoding='utf-8')

    for i in range(66):
        build_movie_question(Question_Training_Dataset)
    print("关于【电影】的训练数据已生成")

    for i in range(99):
        build_celebrity_question(Question_Training_Dataset)
    print("关于【演职人员】的训练数据已生成")

    for i in range(33):
        build_type_question(Question_Training_Dataset)
    print("关于【电影类型】的训练数据已生成")

    for i in range(33):
        build_director_question(Question_Training_Dataset)
    print("关于【导演】的补充训练数据已生成")

    for i in range(33):
        build_writer_question(Question_Training_Dataset)
    print("关于【编剧】的补充训练数据已生成")

    for i in range(22):
        build_actors_question(Question_Training_Dataset)
    print("关于【主演】的补充训练数据已生成")

    Question_Training_Dataset.close()

if __name__ == '__main__': 
    get_name()
    print("\nQuestion_Entity 提取完毕\n")

    build_question()
    print("\nQuestion_Training_Dataset 生成完毕\n")