'''
Descripttion: 
version: 1.0
Author: Ga1axy_z
Date: 2023-02-22 17:55:19
LastEditors: Ga1axy_z
LastEditTime: 2023-02-22 20:07:16
'''
# 各类问题所对应的数据库查询语句
def get_query_template(Category) :
    # 关于【电影】的查询模板
    if Category == "电影别名" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Another_Name"     # query result : "流浪地球：飞跃2020特别版"
    elif Category == "电影海报" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Poster"           # query result : "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2545472803.webp"
    elif Category == "电影时长" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Duration"
    elif Category == "电影上映时间" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Release_Date"
    elif Category == "电影豆瓣评分" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Rating"
    elif Category == "电影涉及的语言" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Language"
    elif Category == "电影剧情简介" :
        return "MATCH (m:Movie {{Name: '{}'}}) RETURN m.Summary"
    elif Category == "电影的导演" :
        return "MATCH (m)-[r:Directed_By]->(p) WHERE m.Name = '{}' RETURN p.Ch_Name"
    elif Category == "电影的编剧" :
        return "MATCH (m)-[r:Written_By]->(p) WHERE m.Name = '{}' RETURN p.Ch_Name"
    elif Category == "电影的主演" :
        return "MATCH (m)-[r:Starred_By]->(p) WHERE m.Name = '{}' RETURN p.Ch_Name"
    elif Category == "电影的类型" :
        return "MATCH (m)-[r:Genre_In]->(n) WHERE m.Name = '{}' RETURN n.Name"
    # 关于【演职人员】的查询模板
    elif Category == "外文名" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Eng_Name"            # query result : "Baoqiang Wang"
    elif Category == "性别" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Gender"
    elif Category == "星座" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Constellation"
    elif Category == "海报" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Poster"
    elif Category == "生日" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Birthday"
    elif Category == "出生地" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Birthplace"
    elif Category == "所有职业" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Occupation"
    elif Category == "个人简介" :
        return "MATCH (p {{Ch_Name: '{}'}}) RETURN p.Description"
    # 关于【电影类型】的查询模板
    elif Category == "类型包括的电影" :
        return "MATCH (m)-[r:Genre_In]-(n) WHERE n.Name = '{}' RETURN m.Name LIMIT 10"
    # 关于【导演】的补充查询模板
    elif Category == "导演执导的电影" :
        return "MATCH (m)-[r:Directed_By]-(p) WHERE p.Ch_Name = '{}' RETURN m.Name LIMIT 10"
    # 关于【编剧】的补充查询模板
    elif Category == "编剧编写的电影" :
        return "MATCH (m)-[r:Written_By]-(p) WHERE p.Ch_Name = '{}' RETURN m.Name LIMIT 10"
    # 关于【主演】的补充查询模板
    elif Category == "演员主演的电影" :
        return "MATCH (m)-[r:Starred_By]-(p) WHERE p.Ch_Name = '{}' RETURN m.Name LIMIT 10"

# 根据问句的分类和问句的对象构造 Neo4j 查询语句
def bulid_query_statement(Category, Entity) :
    return get_query_template(Category).format(Entity)

if __name__ == '__main__' : 
    print(bulid_query_statement("演员主演的电影", "周星驰"))               # MATCH (m)-[r:Starred_By]-(p) WHERE p.Ch_Name = '周星驰' RETURN m.Name LIMIT 10