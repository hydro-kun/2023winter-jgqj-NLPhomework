'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-03-03 09:00:55
LastEditors: Ga1axy_z
LastEditTime: 2023-03-07 12:43:09
'''

# 知识图谱可视化数据接口

from py2neo import Graph

# 连接 Neo4j 数据库
def connect_neo4j() :
    graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    return graph

# 查询 Neo4j 数据库
def query_neo4j(query_statement) :
    graph = connect_neo4j()
    results = graph.run(query_statement)
    return results

def get_echarts_data() :
    # 查询所有节点和关系
    query = """
            MATCH (m:Movie)-[:Directed_By]->(d:Director),
                (m:Movie)-[:Written_By]->(w:Writer),
                (m:Movie)-[:Starred_By]->(a:Actor),
                (m:Movie)-[:Genre_In]->(g:Genre)
            RETURN m, d, w, a, g
            LIMIT 520
            """

    # 构造 EChart 需要的 JSON 数据
    json_data = {
        "nodes": [],
        "links": []
    }

    # 添加节点
    results = query_neo4j(query)
    for record in results:
        for node_type in ["m", "d", "w", "a", "g"]:
            node = record[node_type]
            if "Name" in node and node["Name"] != "" or "Ch_Name" in node and node["Ch_Name"] != "":
                if node_type == "m" :
                    name = ("《" + node["Name"] + "》")
                elif node_type == "g" :
                    name = node["Name"]
                else :
                    name = node["Ch_Name"]
                node_dict = {
                    "id": str(node.identity),
                    "name": name,
                    "type": node_type
                }
                if node_dict not in json_data["nodes"]:
                    json_data["nodes"].append(node_dict)

    # 添加关系
    results = query_neo4j(query)        # 这里 results 使用过一次以后就会自己消失？！
    for record in results:
        json_data["links"].append({
            "source": str(record["m"].identity),
            "target": str(record["d"].identity),
            "relationship": "Directed_By"
        })
        json_data["links"].append({
            "source": str(record["m"].identity),
            "target": str(record["w"].identity),
            "relationship": "Written_By"
        })
        json_data["links"].append({
            "source": str(record["m"].identity),
            "target": str(record["a"].identity),
            "relationship": "Starred_By"
        })
        json_data["links"].append({
            "source": str(record["m"].identity),
            "target": str(record["g"].identity),
            "relationship": "Genre_In"
        })

    # 将 nodes 转换为 ECharts 可读取的数据格式
    # nodes = [{"id": node['id'], 'name': node['name'], 'symbolSize': 30, 'category': node['type']} for node in json_data['nodes']]
    nodes = []
    for node in json_data['nodes'] :
        temp = {}
        temp["id"] = node['id']
        temp["name"] = node['name']
        temp["category"] = node['type']
        if node['type'] == 'm' :
            temp['symbolSize'] = 60             # 设置不同节点的大小
        elif node['type'] == 'd' :
            temp['symbolSize'] = 45
        elif node['type'] == 'w' :
            temp['symbolSize'] = 35
        elif node['type'] == 'a' :
            temp['symbolSize'] = 40
        elif node['type'] == 'g' :
            temp['symbolSize'] = 50
        nodes.append(temp)

    # 将 links 转换为 ECharts 可读取的数据格式
    links = [{'source': link['source'], 'target': link['target'], 'name': link['relationship']} for link in json_data['links']]

    # 生成 ECharts 所需的 JSON 数据
    echarts_data = {'nodes': nodes, 'links': links}

    return echarts_data

if __name__ == '__main__' :
    get_echarts_data()