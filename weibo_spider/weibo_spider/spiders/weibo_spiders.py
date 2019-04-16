#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行环境：Anaconda python 3.6.8
@Created on 2019-4-15 19:44
@Author:ChileWang
@algorithm：
爬取《财上海》微博内容
"""
import scrapy
from weibo_spider.items import WeiboSpiderItem


class MicroBlogSpiders(scrapy.Spider):
    name = "micro_blog_spiders"  # 爬虫名称
    allowed_domains = ["weibo.com"]  # 允许域名
    start_url = ['https://weibo.com/u/1565668374']  # 爬虫的域名开口

    def parse(self, response):
        micro_blog_detail_list_position = response.xpath('.//*/div[@class="WB_detail"]')  # 微博详情页面定位
        for blog_detail in micro_blog_detail_list_position:
            nick_name = blog_detail.xpath('./div[@class="WB_info"]/a/text()').extract()[0]   # 提取昵称  extract()函数用于提取
            publish_time = blog_detail.xpath('./div[@class="WB_from S_txt2"]/a/@title').extract()[0]  # 提取昵称
            try:
                # 微博长文显示不全，需要提取其url去到详情页打开，然后再提取
                micro_blog_url = blog_detail.xpath('./div[@class="WB_text W_f14"]/div[@class="WB_text_opt"]/@href').extract()[0]
                item = WeiboSpiderItem(nick_name=nick_name, publish_time=publish_time)
                request = scrapy.Request(url=micro_blog_url, callback=self.parse_detail)
                request.meta['item'] = item  # 将item暂存
                yield request  # 跳转至详情页
            except Exception as err:
                # 不是微博长文,直接提取正文即可
                micro_blog_text = blog_detail.xpath('./div[@class="WB_text W_f14"]/text()').extract()[0]
                item = WeiboSpiderItem(nick_name=nick_name, publish_time=publish_time, micro_blog_text=micro_blog_text)
                print(err)
                yield item  # 将提取好的所有信息返回items类，完成一条微博的爬取

        # 构建下一页的链接
        next_page = 'https://weibo.com/u/1565668374?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='
        for i in range(2, 501):
            next_page_url = next_page + str(i)
            try:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            except Exception as err:
                print(err)

    def parse_detail(self, response):
        """
        提取微博长文
        :param self:
        :param response: 点击微博长文详情链接url返回的页面
        :return:
        """
        micro_blog_text = response.xpath('.//*div[@class="WB_text W_f14"]/text()').extract()[0]  # 提取微博长文

        # 重新构造item
        item = response.meta['item']
        nick_name = item['nick_name']
        publish_time = item['publish_time']
        print(nick_name)
        print(publish_time)
        print(micro_blog_text)
        item = WeiboSpiderItem(nick_name=nick_name, publish_time=publish_time, micro_blog_text=micro_blog_text)
        yield item  # 将提取好的微博长文所有信息返回items类，完成一条微博长文的爬取


