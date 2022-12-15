from math import*
import matplotlib.pyplot as plt
from sympy import symbols, solve

# 常量赋值
S_eL=67500
a=141040
b=-0.1822
G=11.5*10**6

# 定义运算函数
def calculate_params(N_a, F_max, F_min, k, d):
    C=(d*G/(8*N_a*k))**(1/3)
    D=d*C
    K_1 = 8 * C / (pi * d ** 2)
    K_s = 1 + 1 / (2 * C)
    sigma_L = K_s * F_min * K_1
    F_m = 0.5 * (F_max + F_min)
    sigma_m = K_s * F_m * K_1
    K_omega = (4 * C - 1) / (4 * C - 4) + 0.615 / C
    F_a = 0.5 * (F_max - F_min)
    sigma_a = K_omega * F_a * K_1
    S_u=0.67*a*d**b
    F_s_ = S_eL * (S_u - sigma_L) / (S_eL * (sigma_m - sigma_L) + S_u * sigma_a)
    L_f = d * (N_a + 2) + 1.15 * F_max / k - 0.15 * F_min / k
    F_lim = k * L_f * 0.8125 * (1 - (1 - 6.865 * (C * d / L_f) ** 2) ** 0.5)
    return F_s_, F_lim, D, L_f

# 定义判断函数
def judgment(N_a, F_max, F_min, k, F_s):
    # 初始化变量d
    d = 0.001

    # 开始循环
    while True:
        # 调用calculate_params()函数，并获取返回值
        F_s_, F_lim, D, L_f = calculate_params(N_a, F_max, F_min, k, d)
        # 判断F_s_是否接近F_s，且F_lim大于F_max
        if F_s_>F_s and F_lim.real > F_max:
            # 满足这两个条件，结束循环
            break
        else:
            # 不满足这两个条件，让d+1，并继续循环
            d += 0.001
    print("弹簧平均直径D=%s,满足条件" % D)
    print("弹簧钢线直径d=%s,满足条件" % d)
    return D, d, L_f

# 定义绘图函数
def draw_tangent(D, x1, y1, x2, y2,x3, y3, x4, y4, x5, y5, x6, y6, r):
    circle2 = plt.Circle((x1, y1), r, color=("black"))
    circle3 = plt.Circle((x2, y2), r, color=("black"))
    ax = plt.gca()
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    # 画两个圆的公切线
    plt.plot([x3,x5],[y3,y5], color=("black"))
    plt.plot([x4,x6],[y4,y6], color=("black"))
    # 设置坐标轴的范围
    ax.set_xlim([-0.7*D, 0.7*D])
    ax.set_ylim([-0.7*D, 0.7*D])

# 求切点
def qiedian(x1, y1, m_):
    x3,y3,x4,y4 = symbols('x3,y3,x4,y4')
    eq1=(x3-x1)**2+(y3-y1)**2-(d/2)**2
    eq2=m_*(x3-x1)-(y3-y1)
    x3,x4=solve([eq1,eq2],[x3,y3])
    return x3[0], x3[1], x4[0], x4[1]

# 计算圆心
def two_dimensional_graph(D, d, L_f):
    plt.figure()
    x0=-D/2
    y0=(L_f-d)/2
    r=d/2
    x1=x0
    x2=-x1
    circle1 = plt.Circle((x0, y0), r, color=("black"))
    ax = plt.gca()
    ax.add_artist(circle1)
    for i in range(int(N_a)):
        y1=y0-(i+1)*((L_f-(N_a+1)*d)/N_a+d)
        y2=y1+d
        m = (y2 - y1) / (x2 - x1)
        m_=-1/m
        x3_, y3_, x4_, y4_=qiedian(x0, y0, m_)
        ax = plt.gca()
        plt.plot([x3_,(D+d)/5],[y3_,y3_], color=("black"))
        plt.plot([x4_,(D+d)/5],[y4_,y3_], color=("black"))
        x3, y3, x4, y4=qiedian(x1, y1, m_)
        x5, y5, x6, y6=qiedian(x2, y2, m_)
        draw_tangent(D, x1, y1, x2, y2,x3, y3, x4, y4, x5, y5, x6, y6, r)
        x0_=-x0
        y0_=y0-(N_a+1)*((L_f-(N_a+1)*d)/N_a+d)+d
        x3_, y3_, x4_, y4_=qiedian(x0_, y0_, m_)
        plt.plot([x3_,-(D+d)/5],[y3_,y4_], color=("black"))
        plt.plot([x4_,-(D+d)/5],[y4_,y4_], color=("black"))
        circle4 = plt.Circle((x0_, y0_), r, color=("black"))
        ax.add_artist(circle4)
    plt.show()



# 定义输入函数
def input_parameter():
    #参数输入
    # 输入相关参数
    N_a, F_max, F_min, k, F_s = map(float, input\
        ("请依次输入弹簧的匝数，最大工作载荷，最小工作载荷，弹簧比，安全系数（中间用逗号隔开）：").split(','))
    return N_a, F_max, F_min, k, F_s

# 定义主函数
if __name__ == '__main__':
    # 输入参数
    N_a, F_max, F_min, k, F_s, =input_parameter()
    # 判断结果
    D, d, L_f=judgment(N_a, F_max, F_min, k, F_s)
    two_dimensional_graph(D, d, L_f)