'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-17 14:32:35
LastEditors: Ga1axy_z
LastEditTime: 2023-02-24 20:55:39
'''

import os
from pathlib import Path

#########################################################################

# 项目根目录
# 我改了一下这里
FILE = Path(__file__).resolve()
Project_Path = os.path.dirname(FILE) + '/'
# print(Project_Path)

#########################################################################

# 【 Github 上的共享数据集】，保存了较为全面的豆瓣网站上电影对应的 ID，爬虫在此获取 ID 后访问相关电影页面爬取数据 
doubanID_Path = Project_Path + 'Data/doubanID.json'

# 不带 Temp 是爬虫生成的原始数据，为了方便处理，需要手动在文件开头加上 '['，在文件结尾删除一个多余的 ',' 并加上 ']' 后，保存为带 Temp 的文件
All_Movies_Info_Path = Project_Path + 'DataExt/All_Movies_Info.json'
All_Movies_Info_Temp_Path = Project_Path + 'Data/All_Movies_Info_Temp.json'

All_Celebrities_Info_Path = Project_Path + 'Data/All_Celebrities_Info.json'
All_Celebrities_Info_Temp_Path = Project_Path + 'Data/All_Celebrities_Info_Temp.json'

# 基于【已爬取的电影】信息，整理出【这些电影相关的所有演职人员】的 ID
All_Celebrities_ID_Path = Project_Path + 'Data/All_Celebrities_ID.txt'

# 保存有爬虫已经爬取过的电影和演职人员信息，以实现断点继续
Acquired_Movies_ID_Path = Project_Path + 'Data/Acquired_Movies_ID.txt'
Acquired_Celebrities_ID_Path = Project_Path + 'Data/Acquired_Celebrities_ID.txt'

# 保存爬虫运行期间当前获取到的网页原始数据，用于 Debug
Temporary_Movie_Page_Path = Project_Path + 'Code_Early_Data_Crawling/Temporary_Data/Test_Movie_Page.txt'
Temporary_Person_Page_Path = Project_Path + 'Code_Early_Data_Crawling/Temporary_Data/Test_Person_Page.txt'
Temporary_Celebrity_Page_Path = Project_Path + 'Code_Early_Data_Crawling/Temporary_Data/Test_Celebrity_Page.txt'

#########################################################################

# 【所有的电影名和演职人员名称】
All_Movies_Name_Pro_Path = Project_Path + 'Question_Entity/All_Movies_Name_Pro.txt'
All_Celebrities_Name_Path = Project_Path + 'Question_Entity/All_Celebrities_Name.txt'

# 【数据库中已保存】的五种实体的所有名称
All_Movies_Name_Path = Project_Path + 'Question_Entity/All_Movies_Name.txt'
All_Directors_Name_Path = Project_Path + 'Question_Entity/All_Directors_Name.txt'
All_Writers_Name_Path = Project_Path + 'Question_Entity/All_Writers_Name.txt'
All_Actors_Name_Path = Project_Path + 'Question_Entity/All_Actors_Name.txt'
All_Genres_Name_Path = Project_Path + 'Question_Entity/All_Genres_Name.txt'

#########################################################################

# 关于【电影】的问题模板
QT_Movie_Another_Name_Path = Project_Path + 'Question_Template/Movie/Another_Name.txt'
QT_Movie_Poster_Path = Project_Path + 'Question_Template/Movie/Poster.txt'
QT_Movie_Duration_Path = Project_Path + 'Question_Template/Movie/Duration.txt'
QT_Movie_Release_Date_Path = Project_Path + 'Question_Template/Movie/Release_Date.txt'
QT_Movie_Rating_Path = Project_Path + 'Question_Template/Movie/Rating.txt'
QT_Movie_Language_Path = Project_Path + 'Question_Template/Movie/Language.txt'
QT_Movie_Summary_Path = Project_Path + 'Question_Template/Movie/Summary.txt'
QT_Movie_Director_Path = Project_Path + 'Question_Template/Movie/Director.txt'
QT_Movie_Writer_Path = Project_Path + 'Question_Template/Movie/Writer.txt'
QT_Movie_Actors_Path = Project_Path + 'Question_Template/Movie/Actors.txt'
QT_Movie_Genre_Path = Project_Path + 'Question_Template/Movie/Genre.txt'

# 关于【演职人员】的问题模板
QT_Celebrity_Eng_Name_Path = Project_Path + 'Question_Template/Celebrity/Eng_Name.txt'
QT_Celebrity_Gender_Path = Project_Path + 'Question_Template/Celebrity/Gender.txt'
QT_Celebrity_Constellation_Path = Project_Path + 'Question_Template/Celebrity/Constellation.txt'
QT_Celebrity_Poster_Path = Project_Path + 'Question_Template/Celebrity/Poster.txt'
QT_Celebrity_Birthday_Path = Project_Path + 'Question_Template/Celebrity/Birthday.txt'
QT_Celebrity_Birthplace_Path = Project_Path + 'Question_Template/Celebrity/Birthplace.txt'
QT_Celebrity_Occupation_Path = Project_Path + 'Question_Template/Celebrity/Occupation.txt'
QT_Celebrity_Description_Path = Project_Path + 'Question_Template/Celebrity/Description.txt'

# 关于【导演】的问题模板，是在【演职人员】的问题模板之上的补充
QT_Director_Directed_Path = Project_Path + 'Question_Template/Director/Directed.txt'

# 关于【编剧】的问题模板，是在【演职人员】的问题模板之上的补充
QT_Writer_Written_Path = Project_Path + 'Question_Template/Writer/Written.txt'

# 关于【主演】的问题模板，是在【演职人员】的问题模板之上的补充
QT_Actors_Starred_Path = Project_Path + 'Question_Template/Actors/Starred.txt'

# 关于【电影类型】的问题模板
QT_Genre_Movie_Path = Project_Path + 'Question_Template/Genre/Movie.txt'

#########################################################################

# 用于【训练和测试朴素贝叶斯分类器】的数据集
Question_Training_Dataset = Project_Path + 'Data/Question_Training_Dataset.txt'
# LTP 模型存放路径
LTP_DATA_DIR = Project_Path + 'Model/'

# KGE数据路径
KGE_Data_path = Project_Path + "Data/KGE_Data/"
Entities_Path = KGE_Data_path + "entities.txt"
Relations_Path = KGE_Data_path + "relations.txt"
Train_Path = KGE_Data_path + "train.txt"
Test_Path = KGE_Data_path + "test.txt"
Valid_Path = KGE_Data_path + "valid.txt"
Raw_Path = KGE_Data_path + "raw.txt"
KGE_Save_Path = KGE_Data_path + 'ckpts'
KGE_Log_Path = KGE_Data_path + 'kge.log'
Json_Directed_By_Path = KGE_Data_path + 'director_to_movie.json'
Json_Genre_In_Path = KGE_Data_path + 'genre_to_movie.json'
Json_Starred_By_Path = KGE_Data_path + 'actors_to_movie.json'
Json_Written_By_Path = KGE_Data_path + 'writer_to_movie.json'
Read_Json_Path = Project_Path + 'Code_KGE_Acceleration/read_neo4j_json.py'
