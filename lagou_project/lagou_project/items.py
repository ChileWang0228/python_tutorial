# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 首页
    job = scrapy.Field()  # 工作
    category = scrapy.Field()  # 工作主类别
    sub_category = scrapy.Field()  # 子类
    job_url_menu = scrapy.Field()  # 具体工作的招聘目录链接

    # 具体工作的招聘信息列表页面
    concrete_job = scrapy.Field()  # 具体工作
    concrete_job_url = scrapy.Field()  # 具体工作链接
    job_position = scrapy.Field()  # 工作地点
    publish_time = scrapy.Field()  # 发布时间
    salary = scrapy.Field()  # 薪水
    work_experience = scrapy.Field()  # 工作经验
    company = scrapy.Field()  # 招聘公司
    company_scale = scrapy.Field()  # 公司规模
    job_label = scrapy.Field()  # 工作内容标签
    company_welfare = scrapy.Field()  # 公司福利

    # 点击concrete_job_url的页面
    job_detail = scrapy.Field()  # 职位描述


