#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行环境：Windows Anaconda python 3.7.2
@Created on 2019-4-18 22:20
@Author:ChileWang
@algorithm：
Python基础教学代码
"""

# # 赋值
# a = 1  # 单变量赋值
# c = b = 1  # 多变量赋值
# print(a)
# print(b, c)

# 变量类型
# name = 'Chile'  # 字符串
# miles = 1000.0  # 浮点型
# num = 100  # 整形
# # 打印变量类型
# print(type(name))
# print(type(miles))
# print(type(num))
#
#
"""
标准数据类型
Python有五个标准的数据类型：
Numbers（数字）
String（字符串）
List（列表）
Tuple（元组）
Dictionary（字典）
"""

# Numbers: int & float
# a = 1  # int
# b = 1.0  # float

# String
# my_name = 'Chile'
# print(my_name[0])  # 打印第0个字符
# print(my_name[1: 3])  # 打印第1个到第2个的字符
# print(my_name[2:])  # 打印第2个到最后一个的字符
# print(my_name[-1])  # 打印倒数第一个字符
#
# List
num_list = [1, 2, 3, 4]
str_list = ['Chile', 'b', 'c']
mix_list = ['a', 1, 1.0, num_list, str_list]
# print(num_list)
# print(str_list)
# print(mix_list)
#
# # Tuple
mix_tuple = ('chile', 111, 2.2, 'a', num_list)  # 不可赋值
# print(mix_list[1])
# print(mix_tuple)
# mix_tuple[1] = 1
#
# Dictionary
# test_dict = {'name': 'Chile', 'age': 18, 'num_list': num_list, 'tuple': mix_tuple}
# print(test_dict)
# print(test_dict.keys())  # 打印键
# print(test_dict.values())  # 打印值
# print(test_dict['name'])
# print(test_dict['num_list'])
# print(test_dict['tuple'])
#
# """
# 数据类型转换
# """
#
tr_a = '1'
int_b = int(tr_a)
str_c = str(int_b)
float_d = float(str_c)
# print(type(tr_a))
# print(type(int_b))
# print(type(str_c))
# print(type(float_d))
#
# tr_list = [1, 2, 3]
# set_a = set(tr_list)  # 列表转集合
# list_b = list(set_a)  # 集合转列表
# print(type(tr_list))
# print(type(set_a))
# print(type(list_b))
#
# """
# 算数运算符
# """
a = 2
b = a + 2
c = a - 1
d = a * b
e = d / c
f = d % c  # 取余
g = 3 // 2  # 整除(向下取整)
h = 2**3  # 求幂
print('a:%d Test format' % a)  # 测试格式化
print('b:%s' % str(b))
print('c:', c)
print('d:', d)
print('e:', e)
print('f', f)
print('g:', g)
print('h:', h)
print('abc %d, dhfjdhfhdh, %s, sjdhsjhdhs, skdjskjsk%f,sdjsdhs' % (1, 'dsd', 1.0))
