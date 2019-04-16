# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义要爬取的字段
    nick_name = scrapy.Field()  # 昵称
    publish_time = scrapy.Field()  # 发布时间
    micro_blog_text = scrapy.Field()  # 正文
