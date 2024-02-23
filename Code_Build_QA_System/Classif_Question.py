'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-16 19:56:45
LastEditors: Ga1axy_z
LastEditTime: 2023-04-20 18:49:26
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import os
import sys                                                                      # 实现在文件夹内部的 Python 文件中应用文件夹外部的 Python 文件，这里既 py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))     # 获取父级目录的路径
sys.path.append(parent_dir)                                                     # 将父级目录的路径添加到 sys.path 中
from File_Path import *

# 训练朴素贝叶斯分类器模型
def train_Naive_Bayes_Classifier() :
    # print("朴素贝叶斯分类器模型初始化中...")
    
    # 读取训练数据集，将其存储 data 列表中
    with open(Question_Training_Dataset, 'r', encoding='utf-8') as f:
        data = f.readlines()

    # 将读取的数据集拆分为问句和标签。问句被存储在列表 X 中，标签被存储在列表 y 中
    X = [d.split(',')[0] for d in data]                 # 问句
    y = [d.split(',')[1].strip() for d in data]         # 问句类别标签

    # 分割数据集，将数据集分为训练集和测试集，训练集用于训练模型，测试集用于评估模型性能
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 特征提取，使用 CountVectorizer 类将问句转换为向量表示
    vectorizer = CountVectorizer()                      # CountVectorizer() 是 Scikit-learn 中的一个【用于文本特征提取的类】
    X_train_vec = vectorizer.fit_transform(X_train)     # fit_transform() 函数将【训练数据】转换为【特征向量】，函数接收一个文本数据列表作为输入，返回一个稀疏矩阵，矩阵的每一行表示一个问句，每一列表示一个单词，矩阵中的每个元素表示该单词在对应的问句中出现的次数
    X_test_vec = vectorizer.transform(X_test)           # transform() 函数将【测试数据】转换为【特征向量】

    # 训练模型，使用 MultinomialNB 类来训练模型
    clf = MultinomialNB()                               # MultinomialNB() 是 Scikit-learn 中的一个【朴素贝叶斯分类器类】
    clf.fit(X_train_vec, y_train)                       # fit() 函数将【训练集中的特征向量】和【相应的标签】输入模型进行训练

    # 评估模型性能
    y_pred = clf.predict(X_test_vec)                    # predict() 函数对测试集进行分类预测
    accuracy = accuracy_score(y_test, y_pred)           # accuracy_score() 函数用来计算训练好的模型在测试集上的准确率
    # print('朴素贝叶斯分类器模型初始化完毕，预计分类准确度:', accuracy, "\n")

    return vectorizer,clf

# 使用模型进行文本分类
def classif_question(text, vectorizer, clf) :
    text_vec = vectorizer.transform([text])         # transform() 函数的参数是一个列表或数组，该列表或数组中的每个元素都表示一个数据样本。数据样本通常是一个字符串或文本数据，在文本分类问题中，可以是一个问句或一个文档
    category = clf.predict(text_vec)                # 使用 predict() 函数对问句进行分类
    # print('Category:', category)                    # 输出分类的结果
    return category

if __name__ == '__main__': 
    vectorizer, clf = train_Naive_Bayes_Classifier()
    while (1) :
        text = input("请输入您关于 电影 / 演员 / 编剧 / 导演 / 电影类型 的问题：")
        if text == "quit" :
            break
        classif_question(text, vectorizer, clf)