import SparkApi

# 以下密钥信息从控制台获取
appid = "dbe4c7b3"  # 填写控制台中获取的 APPID 信息
api_secret = "ZmY1MjY3Njg4Mzk0OGZlMWFlYzA1MWE5"  # 填写控制台中获取的 APISecret 信息
api_key = "af72890c2d2d70e70fb64eddc3df6187"  # 填写控制台中获取的 APIKey 信息

domain = "generalv3.5"  # v3版本
# 云端环境的服务地址
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # v3环境的地址（"wss://spark-api.xf-yun.com/v3.1/chat）

text = []


# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


prompt1 = '''给定电影的剧情简介为："{sentence}"\n根据给定的句子，
    找出所有主演并按以下三元组形式分行作答：(“电影名称“，”Starred_By“，”人名”)\n如果没找出就答：无'''
prompt2 = '''给定电影的剧情简介为："{sentence}"\n根据给定的句子，
    找出所有导演并按以下三元组形式分行作答：(“电影名称“，“Directed_By“，“人名”)\n如果没找出就答：无'''
prompt3 = '''给定电影的剧情简介为："{sentence}"\n根据给定的句子，
    找出所有编剧并按以下三元组形式分行作答：(“电影名称“，“Written_By“，“人名”)\n如果没找出就答：无'''
prompt4 = '''给定电影的剧情简介为："{sentence}"\n根据给定的句子，
    推测电影‘类别’的三元组并按以下形式分行作答：(“电影名称“，”Genre_In“，”类别”)\n如果没找出就答：无'''
rela = ['Written_By', 'Starred_By', 'Directed_By', 'Genre_In']
prompt = [prompt1, prompt2, prompt3, prompt4]


def spark_api(question, i):
    """
    :param question:
    :return:
    """
    s1 = question

    pr = prompt[i].format(sentence=s1)
    question = checklen(getText("user", pr))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    with open("result2.txt", 'a', encoding="utf-8") as f:
        f.write(SparkApi.answer)
        f.write('\n')
    text.clear()
    return SparkApi.answer


if __name__ == '__main__':
    text.clear()
    f = open("All_Movies_Info.txt", 'r', encoding="utf-8")
    lists = []
    for line in f:
        lists.append(line.split('},'))
    L = []
    for l in lists:
        for j in l:
            L.append(j)
    for l in L:
        for i in range(4):
            spark_api(l, i)
