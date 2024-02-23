'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-03-07 12:49:40
LastEditors: Ga1axy_z
LastEditTime: 2023-03-09 15:05:28
'''

# 系统统计可视化接口

from py2neo import Graph
import random

# 连接 Neo4j 数据库
def connect_neo4j() :
    graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    return graph

# 查询 Neo4j 数据库
def query_neo4j(query_statement) :
    graph = connect_neo4j()
    results = graph.run(query_statement).data()
    return results

# 获取【上映年份统计】的数据
def get_releaseDate_chart_data() :

    query = '''
            MATCH (m:Movie)
            WHERE m.Release_Date <> ""
            RETURN m.Release_Date as date, COUNT(m) as movie_count, COLLECT(m.Name) as movie_names
            ORDER BY date
            '''
    
    # 获取所有的上映日期，以及这些日期所对应的当天的电影数量和电影名称
    results = query_neo4j(query)
    release_date = [r['date'] for r in results]
    movie_count = [r['movie_count'] for r in results]
    movie_names_temp = [r['movie_names'] for r in results]

    # 为了便于前端 ECharts 显示，只返回当天上映电影的其中一部的名称
    movie_names = []
    for each in movie_names_temp :
        list_length = len(each)                             # 获取列表长度
        random_index = random.randint(0, list_length - 1)   # 在 0 和列表长度之间生成一个随机整数
        movie_names.append(each[random_index])              # 获取列表中随机一部电影的名字

    # 为了方便返回和使用数据，将这三个列表合成一个返回
    releaseDate_chart_data = []
    releaseDate_chart_data.append(release_date)
    releaseDate_chart_data.append(movie_count)
    releaseDate_chart_data.append(movie_names)

    return releaseDate_chart_data

# 获取【电影类型统计】的数据
def get_category_chart_data() :

    query = '''
            MATCH (g:Genre)<-[:Genre_In]-(m:Movie)
            RETURN g.Name as genre, COUNT(m) as movie_count, collect(m.Name) as movie_names
            '''
    
    # 获取所有的电影类型，以及这些类型所对应的电影数量
    results = query_neo4j(query)
    genre = [r['genre'] for r in results]
    movie_count = [r['movie_count'] for r in results]
    movie_names_temp = [r['movie_names'] for r in results]

    # 为了便于前端 ECharts 显示，只返回当天上映电影的其中一部的名称
    movie_names = []
    for each in movie_names_temp :
        list_length = len(each)                             # 获取列表长度
        random_index = random.randint(0, list_length - 1)   # 在 0 和列表长度之间生成一个随机整数
        movie_names.append(each[random_index])              # 获取列表中随机一部电影的名字

    category_chart_data = []
    category_chart_data.append(genre)
    category_chart_data.append(movie_count)
    category_chart_data.append(movie_names)

    return category_chart_data

# 获取【出演电影数量排行】的数据
def get_topActors_chart_data() :

    query = '''
            MATCH (m:Movie)-[:Starred_By]->(a:Actor)
            RETURN a.Ch_Name as actor, count(m) as movie_count, collect(m.Name) as movie_names
            ORDER BY movie_count DESC
            LIMIT 5
            '''
    
    # 获取出演电影数量前五的演员名单，以及这些演员所对应的电影数量和电影名称
    results = query_neo4j(query)
    actor = [r['actor'] for r in results]
    movie_count = [r['movie_count'] for r in results]
    movie_names_temp = [r['movie_names'] for r in results]

    # 为了便于前端 ECharts 显示，只返回当天上映电影的其中一部的名称
    movie_names = []
    for each in movie_names_temp :
        list_length = len(each)                             # 获取列表长度
        random_index = random.randint(0, list_length - 1)   # 在 0 和列表长度之间生成一个随机整数
        movie_names.append(each[random_index])              # 获取列表中随机一部电影的名字

    topActors_chart_data = []
    topActors_chart_data.append(actor)
    topActors_chart_data.append(movie_count)
    topActors_chart_data.append(movie_names)

    return topActors_chart_data

# 获取【出演电影数量排行】的数据
def get_topDirectors_chart_data() :

    query = '''
            MATCH (m:Movie)-[:Directed_By]->(d:Director)
            RETURN d.Ch_Name as director, count(m) as movie_count, collect(m.Name) as movie_names
            ORDER BY movie_count DESC
            LIMIT 5
            '''
    
    # 获取出演电影数量前五的演员名单，以及这些演员所对应的电影数量和电影名称
    results = query_neo4j(query)
    director = [r['director'] for r in results]
    movie_count = [r['movie_count'] for r in results]
    movie_names_temp = [r['movie_names'] for r in results]

    # 为了便于前端 ECharts 显示，只返回当天上映电影的其中一部的名称
    movie_names = []
    for each in movie_names_temp :
        list_length = len(each)                             # 获取列表长度
        random_index = random.randint(0, list_length - 1)   # 在 0 和列表长度之间生成一个随机整数
        movie_names.append(each[random_index])              # 获取列表中随机一部电影的名字

    topDirectors_chart_data = []
    topDirectors_chart_data.append(director)
    topDirectors_chart_data.append(movie_count)
    topDirectors_chart_data.append(movie_names)

    return topDirectors_chart_data

if __name__ == '__main__' :
    # get_releaseDate_chart_data()
    # get_category_chart_data()
    # get_topActors_chart_data()
    get_topDirectors_chart_data()