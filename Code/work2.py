# 导入需要的库
from faker import Faker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置 matplotlib 的中文字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'

# 生成30个人的中文名字
fake = Faker('zh_CN')
names = [fake.name() for _ in range(30)]

# 定义每门课程的学分
credit = [4.0, 4.0, 3.5, 3.0, 3.0, 2.5]

# 生成30个人的每门课程成绩
scores = np.random.normal(loc=70, scale=15, size=(30, 6))
scores[scores < 0] = 0
scores[scores > 100] = 100

# 计算每位同学的每门课程绩点
gpas = (scores / 10) - 5

# 计算每位同学的平均学分绩点
avg_gpa = (credit * gpas).sum(axis=1) / sum(credit)

# 把姓名，课程成绩和平均学分绩点放到一个数据框中
data = {'姓名': names, '语文': scores[:, 0], '数学': scores[:, 1], '外语': scores[:, 2], '计算机': scores[:, 3], '物理': scores[:, 4], '制图': scores[:, 5], '平均学分绩点': avg_gpa}
df = pd.DataFrame(data)

# 按照平均学分绩点排序，并输出到新的文件rankGrade.csv
df.sort_values(by='平均学分绩点', ascending=False).to_csv('rankGrade.csv', index=False, encoding='gb18030')

# 读入文件rankGrade.csv，计算每科的平均分，最高分，以及每科最高分的人的姓名和成绩
df = pd.read_csv('rankGrade.csv', encoding='gb18030')
mean_scores = df.mean()
max_scores = df.max()
name_scores = df.loc[df.iloc[:, 1:7].idxmax()]

# 输出每输出每科的平均分，最高分，以及每科最高分的人的姓名和成绩等相关成绩分析信息
print('平均分：')
print(mean_scores)
print()
print('最高分：')
print(max_scores)
print()
print('每科最高分的人的姓名和成绩：')
print(name_scores)

# 定义每门课程的名称
course_names = ['语文', '数学', '外语', '计算机', '物理', '制图']

# 计算每科的成绩分布
for i in range(6):
    plt.figure()
    plt.title(course_names[i] + '成绩分布')
    labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
    sizes = []
    sizes.append(np.sum((scores[:, i] >= 0) & (scores[:, i] < 20)))
    sizes.append(np.sum((scores[:, i] >= 20) & (scores[:, i] < 40)))
    sizes.append(np.sum((scores[:, i] >= 40) & (scores[:, i] < 60)))
    sizes.append(np.sum((scores[:, i] >= 60) & (scores[:, i] < 80)))
    sizes.append(np.sum((scores[:, i] >= 80) & (scores[:, i] <= 100)))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')

# 展示图片
plt.show()
