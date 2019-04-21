#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行环境：Ubuntu Anaconda python 3.6.8
@Created on 2019-4-20 17:10
@Author:ChileWang
@algorithm：
爬取明星图片
"""
import scrapy
from crawl_star_image_project.items import CrawlStarImageProjectItem


class CrawlStarSpiders(scrapy.Spider):
    name = "crawl_star"  # 爬虫名称 （唯一）
    allowed_domains = ["win4000.com"]  # 允许域名
    # 首页
    start_urls = [
        'http://www.win4000.com/mt/index1.html'
    ]

    def parse(self, response):
        """
        处理目录页
        :param response: 下载的网页
        :return:
        """
        stars_list_position = response.xpath(".//*[@class='Left_bar']//*/li")  # 明星专题位置
        for star in stars_list_position:
            star_images_url = star.xpath("./a/@href").extract()[0]   # 获取具体的明星图片大全链接
            star_name = star.xpath("./a/p/text()").extract()[0]  # 明星名字
            # star_name = star.xpath("./a/p/text()").extract()[0].split('图片')[0]   # 提取明星名字
            # print(star_images_url, star_name)
            item = CrawlStarImageProjectItem(star_name=star_name, star_images_url=star_images_url)
            request = scrapy.Request(url=star_images_url, callback=self.parse_detail)  # 解析详情页
            request.meta['item'] = item  # 将item暂存
            yield request

        next_page = response.xpath(".//*[@class='next']/@href").extract()  # 下一页链接
        print(next_page)
        print('-------------')
        print()
        if next_page:
            next_page_url = next_page[0]
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        """
        处理明星详情页
        :param response: 下载的网页
        :return:
        """
        # website_name = '深圳市龙华区公共资源交易中心'  # 网站名称
        # publish_time = ''  # 发布时间
        star_introduction = response.xpath(".//*[@class='intro_p']/p/text()").extract()[0]  # 明星简介
        images_url = response.xpath(".//*[@class='Left_bar']//*/li/a/img/@src").extract()  # 图片链接
        print(images_url)
        # 重新构造item
        item = response.meta['item']
        star_name = item['star_name']
        star_images_url = item['star_images_url']

        item = CrawlStarImageProjectItem(star_name=star_name, star_images_url=star_images_url,
                                         star_introduction=star_introduction, images_url=images_url)
        yield item
