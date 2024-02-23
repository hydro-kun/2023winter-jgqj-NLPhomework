'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-16 20:34:13
LastEditors: Ga1axy_z
LastEditTime: 2023-05-20 21:08:03
'''

# 问答系统接口

from Code_Build_QA_System.Identify_Entity import *
from Code_Build_QA_System.Classif_Question import *
from Code_Build_QA_System.Construct_Query_Statement import *
from Code_Build_QA_System.Generate_Answer import *
import File_Path

import re
import os
from pyltp import NamedEntityRecognizer
from pyltp import Segmentor
from pyltp import Postagger

# 生成纠错后的问句
def get_corrected_question(Entity_Name, question) :
    pattern = r'《(.*?)》'
    replaced_str = re.sub(pattern, "《" + Entity_Name + "》", question)
    return replaced_str

# 问答系统服务端主程序
def QA_Server(text, segmentor, postagger, recognizer, vectorizer, clf) :
    
    print("\n用户输入：", text)

    # 读取所有的数据库中爬取有数据的实体名
    All_Exist_Entity_Name = read_names(File_Path.All_Movies_Name_Path) + read_names(File_Path.All_Directors_Name_Path) + read_names(File_Path.All_Writers_Name_Path) + read_names(File_Path.All_Actors_Name_Path) + read_names(File_Path.All_Genres_Name_Path)
    Genre_Names = read_names(All_Genres_Name_Path)

    if text != None:         # 为空的话就直接跳过，节约时间
        # 从问句中提取出命名实体
        Entity_Names = identify_entity_name(text, segmentor, postagger, recognizer)
        question = None

        if len(Entity_Names) == 0 :
            print("很抱歉，我没能识别出您想查找的人名，我会继续改进的 (⋟﹏⋞)\n")
            return ["很抱歉，我没能识别出您想查找的信息，我会继续改进的 (⋟﹏⋞)"], None
        elif len(Entity_Names) == 1 :
            Answer = []

            Entity_Name = Entity_Names[0]
            if Entity_Name not in All_Exist_Entity_Name :                                # 如果提取出的实体名不在数据库中则直接返回
                print("很抱歉，我没能找到您需要的信息，我会继续改进的 (˘•︹•˘)\n")
                return ["很抱歉，我没能找到您需要的信息，我会继续改进的 (˘•︹•˘)"], None
            else :
                if Entity_Name not in Genre_Names :                                      # 对于电影相关问句和演职人员相关问句使用朴素贝叶斯分类器进行问句分类
                    tips = False
                    question = basic_correct(text)                                       # 一般不会纠正实体名
                    # question = text # Debug
                    if question != text :                                                # 如果对文本进行了错字纠正
                        tips = True
                    if movie_or_person_or_genre(text) == "Movie" and split_movie_name(text) != Entity_Name : # 或者对电影名进行了模糊搜索且只有一个相似的电影名称
                        tips = True
                    if tips == True :
                        question = get_corrected_question(Entity_Name, question)         # 则进行初步问句纠正，返回实际搜索的问句，提高问句分类准确度
                        print("您是不是想问：", question)
                    # 获取问句类型
                    Question_Category = classif_question(question, vectorizer, clf)
                else :                                                                   # 对于某个类型有哪些电影这一类的问句，直接使用关键词匹配的方式映射到该问句类型中
                    Question_Category = "类型包括的电影"

                # 通过实体名和问句类型构造数据库查询语句
                Query_Statement = bulid_query_statement(Question_Category, Entity_Name)
                # 查询数据库生成回答
                Answer.append(generate_answer(Entity_Name, Question_Category, Query_Statement))

                print(Answer, '\n')
                if question != text : 
                    return Answer, question
                else :
                    return Answer, None
        else :
            Answer = []

            for Entity_Name in Entity_Names :
                if Entity_Name not in All_Exist_Entity_Name :                                       # 如果提取出的实体名不在数据库中则直接返回
                    continue
                else :
                    tips = False
                    question = basic_correct(text)                                                  # 一般不会纠正实体名
                    # question = text # Debug
                    if question != text :                                                           # 如果对文本进行了错字纠正
                        tips = True
                    if movie_or_person_or_genre(text) == "Movie" and split_movie_name(text) != Entity_Name : # 或者对电影名进行了模糊搜索
                        tips = True
                    if tips == True :
                        question = get_corrected_question(Entity_Name, question)                    # 初步问句纠正，提高问句分类准确度
                        print("您是不是想问：", question)

                    # 获取问句类型
                    Question_Category = classif_question(question, vectorizer, clf)
                    # 通过实体名和问句类型构造数据库查询语句
                    Query_Statement = bulid_query_statement(Question_Category, Entity_Name)
                    # 查询数据库生成回答
                    Answer.append(generate_answer(Entity_Name, Question_Category, Query_Statement))

            if Answer != [] :
                print(Answer, '\n')
                if question != text : 
                    return Answer, question
                else :
                    return Answer, None
            else :              # 如果所有相关的模糊实体名都没检索到结果
                print("很抱歉，我没能找到您需要的信息，我会继续改进的 (˘•︹•˘)\n")
                if question != text : 
                    return ["很抱歉，我没能找到您需要的信息，我会继续改进的 (˘•︹•˘)"], question
                else :
                    return ["很抱歉，我没能找到您需要的信息，我会继续改进的 (˘•︹•˘)"], None

if __name__ == '__main__' :

    print("\n问答系统初始化中...")
    # 加载 LTP 模型
    LTP_DATA_DIR = File_Path.LTP_DATA_DIR                                           # 模型文件路径
    segmentor = Segmentor(os.path.join(LTP_DATA_DIR, 'cws.model'))                  # 分词模型
    postagger = Postagger(os.path.join(LTP_DATA_DIR, 'pos.model'))                  # 词性标注模型
    recognizer = NamedEntityRecognizer(os.path.join(LTP_DATA_DIR, 'ner.model'))     # 命名实体识别模型
    # 训练 朴素贝叶斯分类器 模型
    vectorizer, clf = train_Naive_Bayes_Classifier()
    print("久等了，问答系统初始化完毕\n")

    QA_Server("《流浪地球》是什么类型的电影", segmentor, postagger, recognizer, vectorizer, clf)