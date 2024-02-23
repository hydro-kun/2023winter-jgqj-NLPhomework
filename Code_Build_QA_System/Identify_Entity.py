# -*- coding: utf-8 -*-
'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-19 15:04:27
LastEditors: Ga1axy_z
LastEditTime: 2023-05-08 20:49:43
'''
from pycorrector import Corrector
import os
from pyltp import NamedEntityRecognizer
from pyltp import Segmentor
from pyltp import Postagger
import ahocorasick
import re

import sys                                                                      # 实现在文件夹内部的 Python 文件中应用文件夹外部的 Python 文件，这里既 File_Path.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))     # 获取父级目录的路径
sys.path.append(parent_dir)                                                     # 将父级目录的路径添加到 sys.path 中
from File_Path import *

# 纠正电影名称等专有名词的效果不好，但是可以改正问句中的错别字
def basic_correct(question) :
    corrector = Corrector()
    corrected_question, detail = corrector.correct(question)
    # print(detail, "\n")
    return corrected_question

# 读取文件中的每一行，组成一个列表
def read_names(file_path) :
    with open(file_path, 'r', encoding='utf-8') as f :
        names = [line.strip() for line in f]
    return names

# 通过识别问句中是否有书名号《》，以此判断是对 电影实体 进行提取还是对 人员实体 进行提取
def movie_or_person_or_genre(question) :

    genre_names = read_names(All_Genres_Name_Path)

    if question.find("《") != -1 and question.find("》") != -1 :
        return "Movie"
    else:
        for genre in genre_names :
            if question.find(genre) != -1 :
                return genre
        return "Celebrity"

# 切割出书名号《》中包裹的内容，以便在精准匹配无果的情况下进行模糊匹配
def split_movie_name(question) :
    movie_name = re.findall(r'《(.*?)》', question)
    return movie_name[0]

# 创建 AC 自动机
def init_AC_Automaton() :
    names = read_names(All_Movies_Name_Path)
    ac = ahocorasick.Automaton()                # 创建 AC 自动机对象
    for index, name in enumerate(names) :       # 将所有的电影名称添加到到 AC 自动机中
        ac.add_word(name, (index, name))
    ac.make_automaton()                         # 构建 AC 自动机
    return ac

# 使用 AC 自动机在【输入的问句中】对 电影命名实体 进行精准匹配
def get_movie_entity_by_AC_Automaton(question) :

    movie_name = split_movie_name(question)
    ac = init_AC_Automaton()

    Entity_Name = []

    # 在问句中搜索所有电影名，end_index 表示匹配项在问句中的结束位置，insert_order 表示匹配项在 AC 自动机中的插入顺序，original_value 是匹配项本身
    for end_index, (insert_order, original_value) in ac.iter(movie_name) :
        if len(original_value) == len(movie_name) :             # 必须要精准匹配
            # print("命名实体：" + original_value)
            Entity_Name.append(original_value)
    
    if Entity_Name == [] :
        return "Need Fuzzy"
    else :
        return Entity_Name

# 对【提取的电影名称】分词后，将分出来的词语逐个在所有电影名称的词表中进行模糊匹配，最后返回长度与用户输入电影名称长度相同的前三个电影名
def get_movie_entity_by_Fuzzy(question, segmentor, postagger) :

    names = read_names(All_Movies_Name_Path)
    movie_name = split_movie_name(question)

    words = list(segmentor.segment(movie_name))                 # 分词
    postags = list(postagger.postag(words))                     # 词性标注

    Entity_Name = []
    KeyWords = []

    # 对用户输入的电影名进行分词，由于分词得到的部分词语出现频率过高，如 '和'、'一' 等...，它们不具有代表性，故排除掉这些词性的词语
    for word, pos in zip(words, postags) :
        print("分词结果：" + word + '\t' + pos)
        if pos != 'c' and pos != 'b' and pos != 'e' and pos != 'g' and pos != 'h' and pos != 'k' and pos != 'm' and pos != 'p' and pos != 'q' and pos != 'u' and pos != 'wp' and pos != 'x' :
            KeyWords.append(word)

    # 在词库中搜索所有分词得到的词语相关的电影名，限定返回电影名的长度可以实现错字纠正，如 '流浪气球' 纠正为 '流浪地球'，但是如缺字多字的错误则无法识别
    for KeyWord in KeyWords :                                       # 对分词逐个进行检索
        for name in names :                                         # 逐个访问词典文件中的每一行
            if KeyWord in name and len(name) == len(movie_name) :   # 如果分词在某个电影名中出现，且该电影名与用户输入的电影名长度相同
                Entity_Name.append(name)

    # 返回前 3 个元素，如果列表长度不足 3 个，则返回整个列表
    if len(Entity_Name) > 3 :
        return Entity_Name[:3]
    else :
        return Entity_Name

# 使用 NER 库对 人员 进行 命名实体识别
def get_person_entity_by_LTP(question, segmentor, postagger, recognizer) :      # 用 LTP 识别电影名称实现较为困难，但是识别人名准确度还可以
    
    words = list(segmentor.segment(question))                       # 分词
    postags = list(postagger.postag(words))                         # 词性标注
    netags = list(recognizer.recognize(words, postags))             # 命名实体识别

    Entity_Name = []

    # 输出命名实体
    for word, ntag in zip(words, netags) :
        if ntag != 'O' :
            # print("命名实体：" + word + '\t' + ntag)
            Entity_Name.append(word)

    # if Entity_Name == [] :
    #     print("很抱歉，我没能识别出您想查找的人名，我会继续改进的 (⋟﹏⋞)\n")

    return Entity_Name

# 实体抽取主程序
def identify_entity_name(question, segmentor, postagger, recognizer) :
    
    if movie_or_person_or_genre(question) == 'Movie' :              # 问句的对象是电影

        ac_result = get_movie_entity_by_AC_Automaton(question)      # 首先使用 AC 自动机进行精准匹配，比分词再模糊匹配要快一点

        if ac_result == "Need Fuzzy" :                              # 如果精准匹配无结果的话，再进行模糊匹配
            result = get_movie_entity_by_Fuzzy(question, segmentor, postagger)
        else :                                                      # 如果精准匹配有结果的话，直接返回结果
            result = ac_result
        
    elif movie_or_person_or_genre(question) == 'Celebrity' :        # 问句的对象是人员

        result =  get_person_entity_by_LTP(question, segmentor, postagger, recognizer)      # 使用 LTP 直接提取命名实体

    else :                                                          # 问句的对象是电影类型

        result = []
        result.append(movie_or_person_or_genre(question))           # 直接返回匹配到的电影类型名称

    return result

if __name__ == '__main__' : 

    # 加载 LTP 模型
    LTP_DATA_DIR = './Model'                                                        # 模型文件路径
    segmentor = Segmentor(os.path.join(LTP_DATA_DIR, 'cws.model'))                  # 分词模型
    postagger = Postagger(os.path.join(LTP_DATA_DIR, 'pos.model'))                  # 词性标注模型
    recognizer = NamedEntityRecognizer(os.path.join(LTP_DATA_DIR, 'ner.model'))     # 命名实体识别模型

    while (1) :
        text = input("请输入您关于 电影 / 演员 / 编剧 / 导演 / 电影类型 的问题：")

        if text == "quit" :
            
            # 释放 LTP 模型
            segmentor.release()
            postagger.release()
            recognizer.release()

            break

        print("命名实体：" + ' '.join(identify_entity_name(text, segmentor, postagger, recognizer)) + '\n')