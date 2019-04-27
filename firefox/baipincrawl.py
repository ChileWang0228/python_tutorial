#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : baipincrawl.py
@Author: Gu kun
@Date  : 19-4-18 下午1:54
@Desc  : 
"""
from selenium import webdriver
import time
import random
import json
import urllib.request


def zhaopin(city, position):
    try:
        brower.get("https://zhaopin.baidu.com/quanzhi?city=" +
                   urllib.request.quote(city) + "&query=" + urllib.request.quote(position))   # 打开当前职业和城市的列表首页
    except:
        brower.get("https://zhaopin.baidu.com/quanzhi?city=" +
                   urllib.request.quote(city) + "&query=" + urllib.request.quote(position))
    time.sleep(2)


    all_window_height = []
    all_window_height.append(brower.execute_script("return document.body.scrollHeight;"))  # 当前页面的最大高度加入列表
    while True:
        brower.execute_script("scroll(0,100000)")  # 执行拖动滚动条操作
        time.sleep(random.randint(5, 10))
        check_height = brower.execute_script("return document.body.scrollHeight;")  # 记录现在的滚动条长度
        if check_height == all_window_height[-1]:  # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
            break
        else:
            all_window_height.append(check_height)

    response_free = brower.find_elements_by_xpath('//a[@href="javascript:void(0)"]/div[1]')  # 找到列表页中关于具体职位的链接所在的元素
    url_set = set()
    for i in response_free:       # 提取出具体职位的链接，存入集合中
        context_url = i.get_attribute('data-click')
        url = eval(context_url)['url']
        url_set.add(url)
    time.sleep(5)
    
    for j in url_set:    # 访问每一个具体职业的页面
        try:
            brower.get(j)
        except:
            brower.refresh()
        time.sleep(3)
        try:
            brower.find_element_by_class_name('job-description-more').click()    # 找到可能存在的展开全部并点击
        except:
            pass
        time.sleep(2)
        try:
            a = {}
            a['position'] = brower.find_element_by_xpath('//h4[@class="job-name"]').text
            a['company'] = brower.find_element_by_xpath('//h4[@class="bd-tt"]').text
            a['degree'] = brower.find_element_by_xpath('//div[@class="job-require"]').text
            a['salary'] = brower.find_element_by_xpath('//span[@class="salary"]').text
            a['job_description'] = brower.find_element_by_xpath('//div[@class="job-description"]').text
            a['job_type'] = brower.find_element_by_xpath('//div[@class="job-classfiy"]/p[1]').text
            a['time'] = brower.find_element_by_xpath('//div[@class="job-classfiy"]/p[2]').text
            a['location'] = brower.find_element_by_xpath('//div[@class="job-classfiy"]/p[5]').text
            alit = json.dumps(a, ensure_ascii=False)
            line = alit + '\n'
            fo.write(line)
        except:
            pass


brower = webdriver.Firefox()
brower.get("https://zhaopin.baidu.com/")
time.sleep(240)  # 手动登入成功回到起始页即可，预留4分钟操作时间
positions = ['程序员', '网页设计', '技术专员', '软件工程师', '测试工程师', '运维工程师', '技术支持', '硬件工程师', '系统工程师',
             '通信工程师', '数据工程师', '前端工程师', 'APP开发', '算法工程师',  '产品管理', '产品运营', '产品助理', '项目经理',
             '高级产品经理', '产品实习生', 'SEO' '无线电', '电路工程', '自动化', '电子维修', '产品工艺']
cities = ['北京', '天津', '太原', '大同', '呼和浩特', '包头', '石家庄', '廊坊', '邯郸', '上海', '杭州', '宁波', '温州', '南京',
          '济南', '青岛', '台州', '嘉兴', '金华', '绍兴', '苏州', '无锡', '常州', '南通', '扬州', '徐州', '连云港', '福州', '厦门',
          '泉州', '烟台', '潍坊', '临沂', '淄博', '菏泽', '威海', '合肥', '马鞍山', '芜湖', '广州', '深圳', '海口', '三亚', '南宁',
          '桂林', '玉林', '百色', '武汉', '南昌', '郑州', '长沙', '九江', '赣州', '株洲', '常德', '宜昌', '十堰', '荆州', '洛阳',
          '南阳', '新乡', '安阳', '重庆', '成都', '绵阳', '贵阳', '遵义', '昆明', '大理', '拉萨', '西安', '宝鸡', '西宁', '银川',
          '兰州', '咸阳', '天水', '乌鲁木齐', '昌吉', '固原', '沈阳', '大连', '哈尔滨', '长春', '吉林', '朝阳', '锦州', '四平',
          '大庆', '牡丹江']

for position in positions:
    fo = open('{}.json'.format(position), 'at')
    for city in cities:
        zhaopin(city, position)
    fo.close()


