# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlStarImageProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 目录页
    star_name = scrapy.Field()  # 明星名字
    star_images_url = scrapy.Field()  # 明星图片大全链接

    # 详情页
    star_introduction = scrapy.Field()  # 明星简介
    images_url = scrapy.Field()
    images = scrapy.Field()