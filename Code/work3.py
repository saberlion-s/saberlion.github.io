# 导入需要的库
import requests
import math
from bs4 import BeautifulSoup
import re, os
import jieba
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def spider_page(cid):
    # 拼接哔哩哔哩存储弹幕的XML文件
    url = f'http://comment.bilibili.com/{cid}.xml'
    # 模拟网页请求获取数据
    response = requests.get(url)

    # 将网页内容解析为 BeautifulSoup 对象
    soup = BeautifulSoup(response.content, 'html.parser')

    # 创建一个字典来保存每个时间区间的弹幕数量
    time_range_counts = {}

    # 创建一个字典来保存每个用户的弹幕数量
    user_counts = {}

    # 创建一个字符串变量，用于保存所有弹幕的内容
    all_comments = ""

    # 提取所有 d 标签中的内容
    for tag in soup.find_all('d'):
        # 获取 d 标签中的 p 属性
        attributes = tag['p'].split(',')
        # 获取发送时间
        time = attributes[0]
        # 计算时间区间的编号
        time_range_number = int(float(time)) // 60
        # 如果该时间区间已经存在，则将其弹幕数量加 1，否则将其初始化为 1
        time_range_counts[time_range_number] = time_range_counts.get(time_range_number, 0) + 1
        # 获取用户 ID
        user_id = attributes[6]
        # 如果该用户已经存在，则将其弹幕数量加 1，否则将其初始化为 1
        user_counts[user_id] = user_counts.get(user_id, 0) + 1
        # 获取弹幕内容
        content = tag.string
        all_comments += content
        print(time, user_id, content)
    # 根据时间区间的编号排序
    time_ranges = sorted(time_range_counts.keys())

    # 绘制柱状图
    plt.bar(time_ranges, [time_range_counts[time_range] for time_range in time_ranges])
    # 添加横纵坐标的标签
    font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14)
    plt.xlabel("时间区间", fontproperties=font)
    plt.ylabel("弹幕数量", fontproperties=font)
    plt.show()

    # 使用 collections.Counter 类统计弹幕数量最多的10位用户
    from collections import Counter
    top_users = Counter(user_counts).most_common(10)

    # 绘制柱状图
    plt.bar([user[0] for user in top_users], [user[1] for user in top_users])
    # 添加横纵坐标的标签
    plt.xlabel('用户 ID', fontproperties=font)
    plt.ylabel('弹幕数量', fontproperties=font)
    plt.show()

    # 生成词云图
    mask = imread('img_1.png')
    wordcloud = WordCloud(font_path='msyh.ttc', mask=mask).generate(all_comments)

    # 显示词云图
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    cid = '235258065'
    print('正在解析，开始爬取弹幕中。。。。。')
    spider_page(cid)
