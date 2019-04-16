#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行环境：Windows Anaconda python 3.7.2
@Created on 2019-3-28 17:10
@Author:ChileWang
@algorithm：
模拟点击登录 https://m.weibo.cn
"""
import time
import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
pd.set_option('display.max_columns', None)  # 显示所有列


def weibo_crawl():
    """
    爬取微博长文
    :return:
    """
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出默认编码

    url = 'https://m.weibo.cn/u/1565668374'  # 微博主页

    # 使用无头chrome登录
    chrome_options = Options()
    # chrome_options.add_argument('--proxy-server=http://172.31.171.80')
    # chrome_options.add_argument(
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    #     Chrome/73.0.3683.86 Safari/537.36')
    # 无头界面
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # 等待一定时间，用以加载JS脚本
    time.sleep(5)
    # 将页面滚动条拖到底部
    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(2):
        driver.execute_script(js)
        time.sleep(1)
    nick_name = driver.find_elements_by_class_name("m-text-cut")[1].text  # 昵称
    # 定位微博详情链接
    weibo_context_response = driver.find_elements_by_xpath('.//*/div[@class="weibo-text"]/a')

    # elements:返回多个元素 element:返回匹配的第一个元素
    weibo_context_url_list = []  # 微博长文的全文链接列表
    for weibo_context_url in weibo_context_response:
        weibo_context_url = weibo_context_url.get_attribute('href')  # 获取微博长文的全文链接
        weibo_context_url_list.append(weibo_context_url)

    weibo_context_list = []
    publish_time_list = []
    nick_name_list = []
    time_stamp_list = []
    # 提取相应字段
    for weibo_context_url in weibo_context_url_list:
        driver.get(weibo_context_url)
        time.sleep(3)
        weibo_context = driver.find_element_by_class_name('weibo-text').text
        publish_time = driver.find_element_by_class_name('time').text

        weibo_context_list.append(weibo_context)
        publish_time_list.append(publish_time)
        nick_name_list.append(nick_name)
        time_stamp_list.append(int(time.time()))  # 时间戳

    # 多个列表合成csv文件
    show_table = {
        'nick_name': nick_name_list,
        'time_stamp': time_stamp_list,
        'publish_time': publish_time_list,
        'weibo_context_url': weibo_context_url_list,
        'weibo_context': weibo_context_list
    }
    show_table_df = pd.DataFrame(show_table)
    show_table_df.to_csv(nick_name + '_weibo_info.csv', index=False, encoding='UTF-8')  # 不要索引

    # 打印网页源码
    # print(driver.page_source.encode('utf-8').decode())
    driver.quit()


if __name__ == '__main__':
    # weibo_crawl()
    show_table = pd.read_csv('财宝宝_weibo_info.csv', engine='python', encoding='UTF-8')
    print(show_table.head(5))









