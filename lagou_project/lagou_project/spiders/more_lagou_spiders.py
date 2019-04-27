# -*- coding: utf-8 -*-
"""
运行环境：Ubuntu Anaconda python 3.6.8
@Created on 2019-4-24 20:32
@Author:ChileWang
@algorithm：
拉勾网数据
"""
import scrapy
from lagou_project.items import LagouProjectItem
import json


class CrawlStarSpidersIndexPage(scrapy.Spider):
    """
    爬取首页
    """
    name = "lagou_project_index"  # 爬虫名称 （唯一）
    allowed_domains = ["lagou.com"]  # 允许域名
    # 首页
    start_urls = [
        'https://www.lagou.com/'
    ]

    def parse(self, response):
        """
        处理目录页
        :param response: 下载的网页
        :return:
        """
        print(response)
        menu_list_position = response.xpath(".//*[@class='menu_box']")  # 工作分类菜单定位
        for menu in menu_list_position:
            category = menu.xpath(".//*[@class='category-list']/h2/text()").extract()[0]  # 工作主类
            sub_category_list = menu.xpath(".//*[@class='menu_sub dn']/dl/dt/span/text()").extract()  # 工作子类列表
            for sub_cate in sub_category_list:
                sub_category = sub_cate  # 工作子类
                job_url_menu_list = menu.xpath(".//*[@class='menu_sub dn']/dl/dd/a/@href").extract()   # 工作的招聘目录链接列表
                job_list = menu.xpath(".//*[@class='menu_sub dn']/dl/dd/a/text()").extract()   # 工作名字列表

                for i in range(len(job_list)):
                    job = job_list[i]  # 工作
                    job_url_menu = job_url_menu_list[i]  # 工作的招聘目录链接
                    item = LagouProjectItem(job=job, job_url_menu=job_url_menu,
                                            category=category, sub_category=sub_category)
                    print(item)
                    yield item


class CrawlStarSpidersMenu(scrapy.Spider):
    """
    爬取某类工作的目录页面　
    """
    name = "lagou_project_menu"  # 爬虫名称 （唯一）
    allowed_domains = ["lagou.com"]  # 允许域名
    # 首页
    urls = []
    with open("crawl_star_index.json", 'r') as load_f:
        load_dicts = json.load(load_f)
        for l_dict in load_dicts:
            urls.append(l_dict['job_url_menu'])
            break
    start_urls = urls
    print(start_urls)

    def parse(self, response):
        """
        处理工作招聘目录
        :param response: 下载的网页
        :return:
        """
        print('parse_menu')
        print(response)
        concrete_job_list_position = response.xpath(".//*[@class='s_position_list']//*/li")  # 具体工作信息列表定位
        print(concrete_job_list_position)
        for con_job in concrete_job_list_position:
            con_job_top = con_job.xpath("./[@class='list_item_top']")  # 招聘信息顶部
            print(con_job_top)
            concrete_job = con_job_top.xpath(".//*[@class='position']//*/h3/text()").extract()[0]  # 具体工作

            concrete_job_url = con_job_top.xpath(".//*[@class='p_top']/a/@href").extract()[0]  # 具体工作链接
            job_position = con_job_top.xpath(".//*[@class='add']/text()").extract()[0]  # 工作地点
            publish_time = con_job_top.xpath(".//*[@class='format-time']/text()").extract()[0]  # 发布时间
            salary = con_job_top.xpath(".//*[@class='money']/text()").extract()[0]  # 薪水
            work_experience = con_job_top.xpath(".//*[@class='li_b_l']/text()").extract()[0]  # 工作经验
            company = con_job_top.xpath(".//*[@class='company_name']/a/text()").extract()[0]  # 招聘公司
            company_scale = con_job_top.xpath(".//*[@class='industry']/text()").extract()[0]  # 公司规模
            print(concrete_job)

            # 招聘信息底部
            con_job_bot = con_job.xpath("./[@class='list_item_bot']")  # 招聘信息底部
            job_label = con_job_bot.xpath(".//*[@class='li_b_l']/text()").extract()[0]  # 工作内容标签
            company_welfare = con_job_bot.xpath(".//*[@class='li_b_r']/text()").extract()[0]  # 工作福利

            item = LagouProjectItem(concrete_job=concrete_job,
                                    concrete_job_url=concrete_job_url, job_position=job_position,
                                    publish_time=publish_time, salary=salary, work_experience=work_experience,
                                    company=company, company_scale=company_scale, job_label=job_label,
                                    company_welfare=company_welfare)
            print(item)
            yield item
        # 下一页


class CrawlStarSpidersJobDetail(scrapy.Spider):
    name = "lagou_project_job_detail"  # 爬虫名称 （唯一）
    allowed_domains = ["lagou.com"]  # 允许域名
    # 首页
    start_urls = [
            'https://www.lagou.com/'
        ]

    def parse(self, response):
        """
        解析具体的工作页面，提取工作描述
        :param response:
        :return:
        """
        job_detail = response.xpath(".//*[@class='job_detail']/text()").extract()[0]  # 职位描述
        item = LagouProjectItem(job_detail=job_detail)
        print(item)
        yield item



