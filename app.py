'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-24 19:50:19
LastEditors: Ga1axy_z
LastEditTime: 2023-04-20 19:00:44
'''

# app.py 是 Flask 应用程序的入口文件，templates 文件夹用来存放引擎渲染用的网页模板文件，static 文件夹用于存放网页引用的 CSS、JS、图片等静态资源

from Code_Build_QA_System.Identify_Entity import *
from Code_Build_QA_System.Classif_Question import *
from Code_Build_QA_System.Construct_Query_Statement import *
from Code_Build_QA_System.Generate_Answer import *
import File_Path

import os
from pyltp import NamedEntityRecognizer
from pyltp import Segmentor
from pyltp import Postagger

import QA_System_Server
from flask import Flask                     # 导入 Flask 类
from flask import render_template           # 使用 Flask 库里的 Jinja2 模板引擎，通过 render_template 方法，即可将静态的 HTML 文件传入，同时也可以将数据传输到 HTML 文件中显示
from flask import request

import KG_View_Server
import SS_View_Server

import subprocess                           # 导入 subprocess 模块，该模块可以在 Python 中启动一个外部程序，这里用来启动 neo4j start.bat 脚本
import webbrowser                           # 导入 webbrowser 模块，该模块可以自动打开一个指定的超链接，这里用来直接打开 http://127.0.0.1:2023/

app = Flask(__name__)                       # 创建一个 Flask 程序实例

app.config['question'] = app.config['segmentor'] = app.config['postagger'] = app.config['recognizer'] = app.config['vectorizer'] = app.config['clf'] = None

@app.before_first_request                   # init() 函数被装饰为 before_first_request，即它将【仅在第一次请求页面时被调用】，进行一些初始化操作
def init():                                 # 将用到的模型定义为全局变量，这样在整个问答系统的运行过程中只需要加载一次，可以节省大量加载时间

    print("\n问答系统初始化中...             ETA: < 1 min")
    # 加载 LTP 模型
    LTP_DATA_DIR = File_Path.LTP_DATA_DIR                                                         # 模型文件路径
    app.config['segmentor'] = Segmentor(os.path.join(LTP_DATA_DIR, 'cws.model'))                  # 分词模型
    app.config['postagger'] = Postagger(os.path.join(LTP_DATA_DIR, 'pos.model'))                  # 词性标注模型
    app.config['recognizer'] = NamedEntityRecognizer(os.path.join(LTP_DATA_DIR, 'ner.model'))     # 命名实体识别模型
    # 训练 朴素贝叶斯分类器 模型
    app.config['vectorizer'], app.config['clf'] = train_Naive_Bayes_Classifier()
    print("久等了，问答系统初始化完毕\n")

@app.route("/")                             # 定义路由
def index() :                               # 定义视图函数，即定位到该路由时，就调用这个函数，与上面的函数不同，这些函数将在每次请求页面时都被调用

    app.config['question'] = None
    app.config['question'] = request.args.get('Input_Question')     # 在 Flask 应用程序中，request.args.get() 方法用来获取通过 GET 方法传递的数据，如果在 URL 中相应参数不存在，则返回 None

    app.config['knowledge_graph'] = None
    app.config['knowledge_graph'] = request.args.get('knowledge_graph')

    app.config['system_statistics'] = None
    app.config['system_statistics'] = request.args.get('system_statistics')

    if app.config['question'] != None :                 # 如果用户进行了搜索就调用问答系统接口生成回答
        answer, corrected_question = QA_System_Server.QA_Server(app.config['question'], app.config['segmentor'], app.config['postagger'], app.config['recognizer'], app.config['vectorizer'], app.config['clf'])
        return render_template("index.html", answer_num=len(answer), question_answer=answer, input_question=app.config['question'], corrected_question=corrected_question)
    
    elif app.config['knowledge_graph'] != None :        # 如果用户点击知识图谱按钮
        echarts_data = KG_View_Server.get_echarts_data()
        return render_template("index.html", echarts_data=echarts_data, knowledge_graph=True)
    
    elif app.config['system_statistics'] != None :      # 如果用户点击统计数据按钮
        releaseDate_chart_data = SS_View_Server.get_releaseDate_chart_data()
        category_chart_data = SS_View_Server.get_category_chart_data()
        topActors_chart_data = SS_View_Server.get_topActors_chart_data()
        topDirectors_chart_data = SS_View_Server.get_topDirectors_chart_data()
        return render_template("index.html", releaseDate_chart_data=releaseDate_chart_data, category_chart_data=category_chart_data, topActors_chart_data=topActors_chart_data, topDirectors_chart_data=topDirectors_chart_data, system_statistics=True, category_chart=True, releaseDate_chart=True, topActors_chart=True, topDirectors_chart=True)
    
    else :                                              # 如果没有交互，则直接返回初始网页，节约时间
        return render_template("index.html")            # 调用 render_template 函数，传入 HTML 文件参数

if __name__ == "__main__":
    subprocess.Popen([r'neo4j start.bat'], shell=True)  # 调用 Python 标准库中的 subprocess 模块的 Popen 方法，启动 Neo4j 数据库，该方法会在后台运行脚本，因此不会阻塞当前进程
    webbrowser.open_new('http://127.0.0.1:2023/')       # 调用 open_new 方法，自动打开网站
    app.run(port=2023, host="127.0.0.1", debug=True)    # 调用 run 方法，设定端口号，运行 Flask 程序，启动服务