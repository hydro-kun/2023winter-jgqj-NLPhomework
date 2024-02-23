'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-22 17:56:02
LastEditors: Ga1axy_z
LastEditTime: 2023-03-01 20:12:12
'''
from py2neo import Graph

# 连接 Neo4j 数据库
def connect_neo4j() :
    graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    return graph

# 查询 Neo4j 数据库
def query_neo4j(query_statement) :
    graph = connect_neo4j()
    results = graph.run(query_statement).data()
    return results

# 各类问题所对应的回答模板
def get_answer_template(Category) :
    # 关于【电影】的回答模板
    if Category == "电影别名" :
        return "{} 又叫做 {} 哦"
    elif Category == "电影海报" :
        return "你可以在 {} 看到 {} 的海报"         # 注意顺序，poster，movie
    elif Category == "电影时长" :
        return "{} 长达 {}"
    elif Category == "电影上映时间" :
        return "{} 是 {} 上映的"
    elif Category == "电影豆瓣评分" :
        return "{} 的豆瓣评分高达 {} 呢"
    elif Category == "电影涉及的语言" :
        return "在 {} 中出现了如下几种语言：\n{}"
    elif Category == "电影剧情简介" :
        return "{} 的主要剧情如下：\n {}"
    elif Category == "电影的导演" :
        return "{} 的导演是 {} 哦"                  # 一部电影只有一位导演，直接输出就行
    elif Category == "电影的编剧" :
        return "{} 的编剧是："                      # 具体的内容需要循环列表输出
    elif Category == "电影的主演" :
        return "{} 的主要演员包括："                # 具体的内容需要循环列表输出
    elif Category == "电影的类型" :
        return "{} 包含了这些要素：\n"              # 具体的内容需要循环列表输出
    # 关于【演职人员】的回答模板
    elif Category == "外文名" :
        return "{} 的外文名是 {}"
    elif Category == "性别" :
        return "{} 是一名成年 {} 性"
    elif Category == "星座" :
        return "{} 是 {} 的诶"
    elif Category == "海报" :
        return "你可以在 {} 查看 {} 的照片哦"       # 注意顺序，poster，people
    elif Category == "生日" :
        return "{} 的生日是 {}"
    elif Category == "出生地" :
        return "{} 是在 {} 出生的呢"
    elif Category == "所有职业" :
        return "你知道吗？{} 还有这些身份哦：{}"
    elif Category == "个人简介" :
        return "{} 的简介如下：\n {}"
    # 关于【电影类型】的回答模板
    elif Category == "类型包括的电影" :
        return "好的，以下是一些含有 {} 要素的电影：\n"         # 具体的内容需要循环列表输出
    # 关于【导演】的补充回答模板
    elif Category == "导演执导的电影" :
        return "{} 执导过以下一些电影哦：\n"                    # 具体的内容需要循环列表输出
    # 关于【编剧】的补充回答模板
    elif Category == "编剧编写的电影" :
        return "以下这些电影的编剧都是 {} 呢：\n"               # 具体的内容需要循环列表输出
    # 关于【主演】的补充回答模板
    elif Category == "演员主演的电影" :
        return "{} 出演过以下这些电影：\n"                      # 具体的内容需要循环列表输出

# 美化返回多个名字时答案的格式
def optimized_answer_format(answer, answer_content, Category) :
    if Category == '电影的编剧' or Category == '电影的主演' :
        for i, item in enumerate(answer_content):
            if i == len(answer_content) - 1:        # 最后一个元素
                answer += item['p.Ch_Name']
            elif i == len(answer_content) - 2:      # 倒数第二个元素
                answer += item['p.Ch_Name'] + '和'
            else:
                answer += item['p.Ch_Name'] + '、'
        return answer
    elif Category == '电影的类型' :
        for i, item in enumerate(answer_content):
            if i == len(answer_content) - 1:        # 最后一个元素
                answer += item['n.Name']
            elif i == len(answer_content) - 2:      # 倒数第二个元素
                answer += item['n.Name'] + '和'
            else:
                answer += item['n.Name'] + '、'
        return answer
    else:
        for i, item in enumerate(answer_content):
            if i == len(answer_content) - 1:        # 最后一个元素
                answer += item['m.Name']
            elif i == len(answer_content) - 2:      # 倒数第二个元素
                answer += item['m.Name'] + '和'
            else:
                answer += item['m.Name'] + '、'
        return answer

# 将数据库查询结果和回答模板拼接到一起
def generate_answer(Entity, Category, query_statement) :

    answer_content = query_neo4j(query_statement)              # 查询结果
    answer_template = get_answer_template(Category)            # 回答模板

    answer = "很抱歉，我没能找到您需要的信息，我会继续改进的"

    if answer_content == None :
        print(answer)
        return answer
    
    # 关于【电影】的回答模板
    if Category == "电影别名" :
        if answer_content[0]['m.Another_Name'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Another_Name'])
    elif Category == "电影海报" :
        if answer_content[0]['m.Poster'] != '' :
            answer = answer_template.format(answer_content[0]['m.Poster'], Entity)
    elif Category == "电影时长" :
        if answer_content[0]['m.Duration'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Duration'])
    elif Category == "电影上映时间" :
        if answer_content[0]['m.Release_Date'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Release_Date'])
    elif Category == "电影豆瓣评分" :
        if answer_content[0]['m.Rating'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Rating'])
    elif Category == "电影涉及的语言" :
        if answer_content[0]['m.Language'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Language'])
    elif Category == "电影剧情简介" :
        if answer_content[0]['m.Summary'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['m.Summary'])
    elif Category == "电影的导演" :
        if answer_content[0]['p.Ch_Name'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Ch_Name'])
    elif Category == "电影的编剧" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)      # Eg: 肖申克的救赎 的编剧是：斯蒂芬·金和弗兰克·德拉邦特
    elif Category == "电影的主演" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)      # Eg: 肖申克的救赎 的主要演员包括：尼尔·吉恩托利、拉里·布兰登伯格、杰弗里·德曼、詹姆斯·惠特摩、马克·罗斯顿、吉尔·贝罗斯、克兰西·布朗、威廉姆·赛德勒、鲍勃·冈顿、摩根·弗里曼和蒂姆·罗宾斯
    elif Category == "电影的类型" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)
    # 关于【演职人员】的回答模板
    elif Category == "外文名" :
        if answer_content[0]['p.Eng_Name'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Eng_Name'])
    elif Category == "性别" :
        if answer_content[0]['p.Gender'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Gender'])
    elif Category == "星座" :
        if answer_content[0]['p.Constellation'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Constellation'])
    elif Category == "海报" :
        if answer_content[0]['p.Poster'] != '' :
            answer = answer_template.format(answer_content[0]['p.Poster'], Entity)
    elif Category == "生日" :
        if answer_content[0]['p.Birthday'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Birthday'])
    elif Category == "出生地" :
        if answer_content[0]['p.Birthplace'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Birthplace'])
    elif Category == "所有职业" :
        if answer_content[0]['p.Occupation'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Occupation'])
    elif Category == "个人简介" :
        if answer_content[0]['p.Description'] != '' :
            answer = answer_template.format(Entity, answer_content[0]['p.Description'])
    # 关于【电影类型】的回答模板
    elif Category == "类型包括的电影" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)
    # 关于【导演】的补充回答模板
    elif Category == "导演执导的电影" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)
    # 关于【编剧】的补充回答模板
    elif Category == "编剧编写的电影" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)
    # 关于【主演】的补充回答模板
    elif Category == "演员主演的电影" :
        answer = answer_template.format(Entity)
        answer = optimized_answer_format(answer, answer_content, Category)

    return answer

if __name__ == '__main__' :
    # print(query_neo4j("MATCH (m)-[r:Genre_In]-(p) WHERE p.Name = '科幻' RETURN m.Name LIMIT 10"))
    # output:
    # [{'m.Name': '流浪地球2'}, {'m.Name': '24：逆转时空'}, {'m.Name': '海市蜃楼'}, {'m.Name': '前目的地'}, {'m.Name': '卡夫卡'}, {'m.Name': '天外魔花'}, {'m.Name': '星际旅行8：第一类接触'}, {'m.Name': '云的彼端，约定的地方'}, {'m.Name': '星河战队'}, {'m.Name': '科学怪人'}]
    print(generate_answer("王宝强", "演员主演的电影", "MATCH (m)-[r:Starred_By]-(p) WHERE p.Ch_Name = '王宝强' RETURN m.Name LIMIT 10"))
    # print(generate_answer("王宝强", "外文名", "MATCH (n {Ch_Name: '王宝强'}) RETURN n.Eng_Name"))
    # print(generate_answer("流浪地球", "电影的导演", "MATCH (m)-[r:Directed_By]->(p) WHERE m.Name = '肖申克的救赎' RETURN p.Ch_Name"))
    # print(query_neo4j("MATCH (m)-[r:Genre_In]-(n) WHERE n.Name = '科幻' RETURN m.Name LIMIT 10"))