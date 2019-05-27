#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author:ChileWang
@Created On 2019-05-26
@Coding Environment: Anaconda Python 3.7
"""
import random
import matplotlib.pyplot as plt
import pandas as pd
"""
问题：
从某物流中心用多台配送车辆(not limited)向多个客户送货,每个客户的位置和货物需求量一定(8t),每台配送车辆的载重量一定,其一次配送的最大行驶距离一定,要求合理安排车辆配送路线,使目标函数得到优化,并满足以下条件:
(1) 每条配送路径上各客户的需求量之和不超过配送车辆的载重量;(8t)
(2) 每条配送路径的长度不超过配送车辆一次配送的最大行驶距离;(80KM)
(3) 每个客户的需求必须满足,且只能由一台配送车辆送货。
以配送总里程最短为目标函数
"""

"""

一个实例：
某物流中心有2 台配送车辆,其载重量均为8t ,车辆每次配送的最大行驶距离为50km ,配送中心(其编号为0) 与8 个客户之间及8 个客户相互之间的距离dij 、8 个客户的货物需求量qj (i 、j = 1 ,2 , ⋯,8) 均见表1 。要求合理安排车辆配送路线,使配送总里程最短。
采用以下参数:群体规模取20 ,进化代数取25 ,交叉概率取0.9 ,变异概率取0.09 ,变异时基因换位次数取5 , 对不可行路径的惩罚权重取100km ,实施爬山操作时爬山次数取20 。对实例随机求解10 次。
"""


# 遗传算法
class GeneticAlgorithm:
    # -----------初始数据定义---------------------
    # 定义一个24 * 24的二维数组表示配送中心(编号为0)与23个客户之间，以及23个客户相互之间的距离d[i][j]
    d = [[0,33.3,25.5,29.7,25.1,29.1,28.7,37.3,35.3,34.3,29.6,26.8,25.6,33.6,29.3,27.2,33.4,27.9,29.1,32.8,25.9,34.4,33.3,30.4],  # 配送中心（编号为0）到23个客户送货点的距离
         [33.3,0.0,16.1,11.7,15.7,7.9,10.6,2.5,2.4,1.5,6.8,8.8,9.9,4.4,6.2,11.7,9.8,16.0,7.9,3.4,9.6,2.7,4.5,10.1],  # 第1个客户到配送中心和其他22个客户送货点的距离
         [25.5,16.1,0.0,10.8,2.6,9.8,9.3,17.9,17.3,18.2,10.2,10.3,8.5,14.4,11.0,6.4,10.5,5.3,9.7,14.4,9.1,15.0,14.0,8.0],  # 第2个客户到配送中心和其他8个客户送货点的距离
         [29.7,11.7,10.8,0.0,11.0,2.1,2.2,10.9,10.3,11.3,2.5,2.6,4.0,6.8,3.7,2.9,6.6,5.2,2.0,8.3,5.9,6.4,6.4,4.0],
         [25.1,15.7,2.6,11.0,0.0,7.4,6.3,16.3,15.6,16.6,8.6,8.6,6.6,12.8,9.4,4.5,8.9,2.8,8.1,12.8,9.7,12.5,12.3,6.8],
         [29.1,7.9,9.8,2.1,7.4,0.0,2.4,11.2,10.5,11.5,1.2,1.4,2.7,5.1,2.0,3.8,7.3,7.9,2.0,5.2,4.7,4.7,4.6,4.2],
         [28.7,10.6,9.3,2.2,6.3,2.4,0.0,10.3,9.7,10.7,10.7,4.1,5.4,5.9,2.8,3.4,5.4,6.7,1.5,6.1,9.3,5.5,5.5,2.8],
         [37.3,2.5,17.9,10.9,16.3,11.2,10.3,0.0,2.0,3.1,4.9,6.7,8.1,2.5,4.4,9.3,7.6,13.6,5.3,1.2,1.2,1.4,2.8,11.0],
         [35.3,2.4,17.3,10.3,15.6,10.5,9.7,2.0,0.0,1.5,7.2,9.1,11.3,4.7,6.7,12.7,10.4,17.0,7.7,3.5,10.2,3.7,5.0,10.7],
         [34.3,1.5,18.2,11.3,16.6,11.5,10.7,3.1,1.5,0.0,11.8,13.2,11.9,5.3,11.2,12.6,12.6,16.9,11.3,5.3,11.6,6.4,6.4,13.2],
         [29.6,6.8,10.2,2.5,8.6,1.2,10.7,4.9,7.2,11.8,0.0,1.8,3.2,5.0,1.8,4.2,7.7,8.3,1.1,5.1,5.2,4.6,4.5,4.7],
         [26.8,8.8,10.3,2.6,8.6,1.4,4.1,6.7,9.1,13.2,1.8,0.0,1.9,6.4,3.3,2.3,8.2,5.8,3.0,6.6,3.9,6.0,6.0,5.1],
         [25.6,9.9,8.5,4.0,6.6,2.7,5.4,8.1,11.3,11.9,3.2,1.9,0.0,6.9,3.7,3.3,8.2,6.4,3.5,7.0,2.8,7.7,6.4,7.4],
         [33.6,4.4,14.4,6.8,12.8,5.1,5.9,2.5,4.7,5.3,5.0,6.4,6.9,0.0,2.4,6.6,5.6,10.9,6.6,2.1,7.0,1.6,0.3,6.0],
         [29.3,6.2,11.0,3.7,9.4,2.0,2.8,4.4,6.7,11.2,1.8,3.3,3.7,2.4,0.0,6.3,5.5,10.4,2.4,3.3,5.4,2.8,2.7,6.7],
         [27.2,11.7,6.4,2.9,4.5,3.8,3.4,9.3,12.7,12.6,4.2,2.3,3.3,6.6,6.3,0.0,7.2,4.5,3.1,8.5,5.8,9.1,7.4,4.2],
         [33.4,9.8,10.5,6.6,8.9,7.3,5.4,7.6,10.4,12.6,7.7,8.2,8.2,5.6,5.5,7.2,0.0,7.5,5.2,7.4,13.7,7.0,6.9,5.1],
         [27.9,16.0,5.3,5.2,2.8,7.9,6.7,13.6,17.0,16.9,8.3,5.8,6.4,10.9,10.4,4.5,7.5,0.0,7.6,7.6,12.2,12.9,11.8,6.3],
         [29.1,7.9,9.7,2.0,8.1,2.0,1.5,5.3,7.7,11.3,1.1,3.0,3.5,6.6,2.4,3.1,5.2,7.6,0.0,5.1,6.2,4.6,4.5,3.5],
         [32.8,3.4,14.4,8.3,12.8,5.2,6.1,1.2,3.5,5.3,5.1,6.6,7.0,2.1,3.3,8.5,7.4,7.6,5.1,0.0,11.5,1.7,1.6,7.3],
         [25.9,9.6,9.1,5.9,9.7,4.7,9.3,1.2,10.2,11.6,5.2,3.9,2.8,7.0,5.4,5.8,13.7,12.2,6.2,11.5,0.0,9.1,6.5,9.7],
         [34.4,2.7,15.0,6.4,12.5,4.7,5.5,1.4,3.7,6.4,4.6,6.0,7.7,1.6,2.8,9.1,7.0,12.9,4.6,1.7,9.1,0.0,2.5,7.0],
         [33.3,4.5,14.0,6.4,12.3,4.6,5.5,2.8,5.0,6.4,4.5,6.0,6.4,0.3,2.7,7.4,6.9,11.8,4.5,1.6,6.5,2.5,0.0,5.1],
         [30.4,10.1,8.0,4.0,6.8,4.2,2.8,11.0,10.7,13.2,4.7,5.1,7.4,6.0,6.7,4.2,5.1,6.3,3.5,7.3,9.7,7.0,5.1,0.0],
         ]

    # 23个客户分布需要的货物的需求量，第0位为配送中心自己
    q = [0, 2, 2, 2, 3, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 3, 2, 2, 1, 1, 1, 2, 1, 3]

    # 定义一些遗传算法需要的参数
    JCL = 0.9  # 遗传时的交叉率
    BYL = 0.09  # 遗传时的变异率
    JYHW = 5  # 变异时的基因换位次数
    PSCS = 20  # 爬山算法时的迭代次数

    def __init__(self, rows, times, mans, cars, tons, distance, PW):
        self.rows = rows  # 排列个数
        self.times = times  # 迭代次数
        self.mans = mans  # 客户数量
        self.cars = cars  # 车辆总数
        self.tons = tons  # 车辆载重
        self.distance = distance  # 车辆一次行驶的最大距离
        self.PW = PW  # 当生成一个不可行路线时的惩罚因子

    # -------------遗传函数开始执行---------------------
    def run(self):

        print("开始迭代")

        # 路线数组
        lines = [[0 for i in range(self.mans)] for i in range(self.rows)]

        # 适应度
        fit = [0 for i in range(self.rows)]

        # 初始输入获取rows个随机排列，并且计算适应度
        j = 0
        for i in range(0, self.rows):
            j = 0
            while j < self.mans:
                num = int(random.uniform(0, self.mans)) + 1
                if not self.isHas(lines[i], num):
                    lines[i][j] = num
                    j += 1

            # 计算每个线路的适应度
            fit[i] = self.calFitness(lines[i], False)

        # 开始迭代
        t = 0
        while t < self.times:

            # 适应度
            newLines = [[0 for i in range(self.mans)] for i in range(self.rows)]
            nextFit = [0 for i in range(self.rows)]
            randomFit = [0 for i in range(self.rows)]
            totalFit = 0
            tmpFit = 0

            # 计算总的适应度
            for i in range(self.rows):
                totalFit += fit[i]

            # 通过适应度占总适应度的比例生成随机适应度
            for i in range(self.rows):
                randomFit[i] = tmpFit + fit[i] / totalFit
                tmpFit += randomFit[i]

            # 上一代中的最优直接遗传到下一代
            m = fit[0]
            ml = 0

            for i in range(self.rows):
                if m < fit[i]:
                    m = fit[i]
                    ml = i

            for i in range(self.mans):
                newLines[0][i] = lines[ml][i]

            nextFit[0] = fit[ml]

            # 对最优解使用爬山算法促使其自我进化
            self.clMountain(newLines[0])

            # print "开始遗传"
            # 开始遗传
            nl = 1
            while nl < self.rows:
                # 根据概率选取排列
                r = int(self.randomSelect(randomFit))

                # 判断是否需要交叉，不能越界
                if random.random() < self.JCL and nl + 1 < self.rows:
                    fline = [0 for x in range(self.mans)]
                    nline = [0 for x in range(self.mans)]

                    # 获取交叉排列
                    rn = int(self.randomSelect(randomFit))

                    f = int(random.uniform(0, self.mans))
                    l = int(random.uniform(0, self.mans))

                    min = 0
                    max = 0
                    fpo = 0
                    npo = 0

                    if f < l:
                        min = f
                        max = l
                    else:
                        min = l
                        max = f

                    # print "将截取的段加入新生成的基因"
                    # 将截取的段加入新生成的基因
                    """
                    除排在第一位的最优个体外,另N - 1 个个体要按交叉概率Pc 进行配对交叉重组。
                    采用类OX法实施交叉操作,现举例说明其操作方法: 
                    ①随机在父代个体中选择一个交配区域,如两父代个体及交配区域选定为:A = 47| 8563| 921 ,B = 83| 4691|257 ;
                    ②将B 的交配区域加到A 的前面,A 的交配区域加到B 的前面,得:A’= 4691| 478563921 ,B’=8563| 834691257 ;
                    ③在A’、B’中自交配区域后依次删除与交配区相同的自然数,得到最终的两个体为:A”= 469178532 ,B”= 856349127 

                    """
                    while min < max:
                        fline[fpo] = lines[rn][min]
                        nline[npo] = lines[r][min]

                        min += 1
                        fpo += 1
                        npo += 1

                    for i in range(self.mans):
                        if self.isHas(fline, lines[r][i]) == False:
                            fline[fpo] = lines[r][i]
                            fpo += 1

                        if self.isHas(nline, lines[rn][i]) == False:
                            nline[npo] = lines[rn][i]
                            npo += 1

                    # 基因变异
                    self.change(fline)
                    self.change(nline)

                    # print "交叉并且变异后的结果加入下一代"
                    # 交叉并且变异后的结果加入下一代
                    for i in range(self.mans):
                        newLines[nl][i] = fline[i]
                        newLines[nl + 1][i] = nline[i]

                    nextFit[nl] = self.calFitness(fline, False)
                    nextFit[nl + 1] = self.calFitness(nline, False)

                    nl += 2

                # 不需要交叉的，直接变异，然后遗传到下一代
                else:

                    line = [0 for i in range(self.mans)]
                    i = 0
                    while i < self.mans:
                        line[i] = lines[r][i]
                        i += 1

                    # 基因变异
                    self.change(line)

                    # 加入下一代
                    i = 0
                    while i < self.mans:
                        newLines[nl][i] = line[i]
                        i += 1

                    nextFit[nl] = self.calFitness(line, False)
                    nl += 1

            # 新的一代覆盖上一代
            for i in range(self.rows):
                for h in range(self.mans):
                    lines[i][h] = newLines[i][h]

                fit[i] = nextFit[i]
            # print(fit)
            t += 1

        # 提取适应度最高的
        m = fit[0]
        ml = 0

        for i in range(self.rows):
            if m < fit[i]:
                m = fit[i]
                ml = i

        print("迭代完成")
        # 输出结果:
        self.calFitness(lines[ml], True)

        print("最优权值为: %f" % m)
        print("最优结果为:")
        route = dict()  # 行驶路径
        current_load = 0  # 当前车辆的载重
        route_list = []
        route_key = 1
        for i in range(self.mans):
            current_load += self.q[lines[ml][i]]
            if current_load <= self.tons:
                route_list.append(lines[ml][i])

            else:
                route[route_key] = route_list
                route_list = []
                route_list.append(lines[ml][i])
                route_key += 1
                current_load = 0
                current_load += self.q[lines[ml][i]]

        # 加上给最后一个路线图
        route[route_key] = route_list
        print('{车辆编号: [该车的行走路线]}')
        print(route)
        print('-------------')
        return m, route

    # -----------------遗传函数执行完成--------------------

    # -----------------各种辅助计算函数--------------------
    # 线路中是否包含当前的客户
    def isHas(self, line, num):
        for i in range(0, self.mans):
            if line[i] == num:
                return True
        return False

    # 计算适应度,适应度计算的规则为每条配送路径要满足题设条件，并且目标函数即 车辆行驶的总里程越小，适应度越高
    def calFitness(self, line, isShow):

        carTon = 0  # 当前车辆的载重
        carDis = 0  # 当前车辆行驶的总距离
        totalDis = 0

        # ll = []
        r = 1  # 表示当前需要车辆数
        # l = 0
        fore = 0  # 表示正在运送的客户编号
        M = 0  # 表示当前的路径规划所需要的总车辆和总共拥有的车辆之间的差，如果大于0，表示是一个失败的规划，乘以一个很大的惩罚因子用来降低适应度

        # 遍历每个客户点

        # for i in range(0, self.mans):  # 用for循环,索引i不会被if语句改变 例如i=11, i-=1(此时i=10), 下一次循环i直接等于12
        i = 0
        while i < self.mans:

            # 行驶的距离
            newDis = carDis + self.d[fore][line[i]]

            # 当前车辆的载重
            newTon = carTon + self.q[line[i]]

            # 如果已经超过最大行驶距离或者超过车辆的最大载重，切换到下一辆车
            if newDis + self.d[line[i]][0] > self.distance or newTon > self.tons:

                # 下一辆车
                totalDis += carDis + self.d[fore][0]   # 后面加这个d[fore][0]表示需要从当前客户处返程的距离
                r += 1
                fore = 0

                # i -= 1  # 表示当前这个点的配送还没有完成

                carTon = 0
                carDis = 0
            else:
                carDis = newDis
                carTon = newTon
                fore = line[i]
                i += 1
        # 加上最后一辆车的距离和返程的距离

        totalDis += carDis + self.d[fore][0]

        if isShow:
            print('用车数量:', r)
            print("总行驶里程为: %.1fkm" % totalDis)
        else:
            # print "中间过程尝试规划的总行驶里程为: %.1fkm" %(totalDis)
            pass

        # 判断路径是否可用，所使用的车辆数量不能大于总车辆数量
        if r - self.cars + 1 > 0:
            M = r - self.cars + 1

        # 目标函数，表示一个路径规划行驶的总距离的倒数越小越好
        result = 1 / (totalDis + M * self.PW)

        return result

    # 爬山算法
    def clMountain(self, line):
        oldFit = self.calFitness(line, False)

        i = 0
        while i < self.PSCS:
            f = random.uniform(0, self.mans)
            n = random.uniform(0, self.mans)

            self.doChange(line, f, n)

            newFit = self.calFitness(line, False)

            if newFit < oldFit:
                self.doChange(line, f, n)
            i += 1

    # 基因变异
    # 变异的意思是当满足变异率的条件下，随机的两个因子发生多次交换，交换次数为变异迭代次数规定的次数
    def change(self, line):
        if random.random() < self.BYL:
            i = 0
            while i < self.JYHW:
                f = random.uniform(0, self.mans)
                n = random.uniform(0, self.mans)

                self.doChange(line, f, n)
                i += 1

    # 将线路中的两个因子执行交换
    def doChange(self, line, f, n):

        tmp = line[int(f)]
        line[int(f)] = line[int(n)]
        line[int(n)] = tmp

    # 根据概率随机选择的序列
    def randomSelect(self, ranFit):

        ran = random.random()

        for i in range(self.rows):
            if ran < ranFit[i]:
                return i


def random_color():
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#"+color

# -------------入口函数，开始执行-----------------------------
"""
输入参数的的意义依次为
        self.rows = rows                            #排列个数
        self.times = times                          #迭代次数
        self.mans = mans                            #客户数量 23
        self.cars = cars                            #车辆总数 not limited
        self.tons = tons                            #车辆载重 8t
        self.distance = distance                    #车辆一次行驶的最大距离 80KM
        self.PW = PW                                #当生成一个不可行路线时的惩罚因子
"""
if __name__ == '__main__':
    t = 20
    total_distance_list = []
    route_list = []
    time_list = []
    for i in range(300):
        print('迭代次数:%d' % t)
        ga = GeneticAlgorithm(rows=20, times=t, mans=23, cars=2000, tons=8, distance=80, PW=100)
        result = ga.run()
        total_distance_list.append(result[0])
        route_list.append(result[1])
        time_list.append(t)
        t += 200

    pd_dict = {'times': time_list, 'fitness': total_distance_list}
    data_pd = pd.DataFrame(pd_dict)
    data_pd.plot(x='times', y='fitness')
    plt.show()
    plt.savefig('iteration_fit.png')






