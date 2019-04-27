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
import time


class CrawlStarSpiders(scrapy.Spider):
    name = "lagou_project"  # 爬虫名称 （唯一）
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
                try:
                    sub_category = sub_cate  # 工作子类
                    job_url_menu_list = menu.xpath(".//*[@class='menu_sub dn']/dl/dd/a/@href").extract()   # 工作的招聘目录链接列表
                    job_list = menu.xpath(".//*[@class='menu_sub dn']/dl/dd/a/text()").extract()   # 工作名字列表

                    for i in range(len(job_list)):
                        try:
                            job = job_list[i]  # 工作
                            job_url_menu = job_url_menu_list[i]  # 工作的招聘目录链接
                            item = LagouProjectItem(job=job, job_url_menu=job_url_menu,
                                                    category=category, sub_category=sub_category)

                            request = scrapy.Request(url=job_url_menu, callback=self.parse_menu, dont_filter=True)  # 解析工作的招聘目录
                            request.meta['item'] = item  # 将item暂存
                            yield request
                        except Exception:
                            continue  # 继续循环
                except Exception:
                    continue  # 继续循环

    def parse_menu(self, response):
        """
        处理工作招聘目录
        :param response: 下载的网页
        :return:
        """
        try:
            concrete_job_list_position = response.xpath(".//*[@class='item_con_list']/li")  # 具体工作信息列表定位
            for con_job in concrete_job_list_position:
                try:
                    con_job_top = con_job.xpath(".//*[@class='list_item_top']")  # 招聘信息顶部
                    publish_time = con_job_top.xpath(".//*[@class='format-time']/text()").extract()[0]  # 发布时间
                    if ":" not in publish_time:  # 只爬取今天的招聘信息
                        break
                    else:
                        publish_time = time.strftime("%Y-%m-%d ", time.localtime()) + publish_time[:-2]  # 发布时间加上具体日期
                    concrete_job = con_job_top.xpath(".//*[@class='position']//*/h3/text()").extract()[0]  # 具体工作

                    concrete_job_url = con_job_top.xpath(".//*[@class='p_top']/a/@href").extract()[0]  # 具体工作链接
                    job_position = con_job_top.xpath(".//*[@class='add']").xpath('string(.)').extract()[0]  # 工作地点

                    salary = con_job_top.xpath(".//*[@class='money']/text()").extract()[0]  # 薪水
                    work_experience = (con_job_top.xpath(".//*[@class='li_b_l']")).xpath('string(.)').extract()[0].split('\n')[2]   # 工作经验
                    company = con_job_top.xpath(".//*[@class='company_name']/a/text()").extract()[0]  # 招聘公司
                    company_scale = con_job_top.xpath(".//*[@class='industry']/text()").extract()[0]  # 公司规模

                    # 招聘信息底部
                    con_job_bot = con_job.xpath(".//*[@class='list_item_bot']")  # 招聘信息底部
                    job_label = (con_job_bot.xpath(".//*[@class='li_b_l']")).xpath('string(.)').extract()[0]  # 工作内容标签
                    company_welfare = con_job_bot.xpath(".//*[@class='li_b_r']/text()").extract()[0]  # 工作福利

                    # 重新构造item
                    item = response.meta['item']
                    job = item['job']  # 工作
                    category = item['category']   # 工作主类别
                    sub_category = item['sub_category']   # 子类
                    job_url_menu = item['job_url_menu']   # 具体工作的招聘目录链接

                    item = LagouProjectItem(job=job, job_url_menu=job_url_menu,
                                            category=category, sub_category=sub_category, concrete_job=concrete_job,
                                            concrete_job_url=concrete_job_url, job_position=job_position,
                                            publish_time=publish_time, salary=salary, work_experience=work_experience,
                                            company=company, company_scale=company_scale, job_label=job_label,
                                            company_welfare=company_welfare)
                    request = scrapy.Request(url=concrete_job_url, callback=self.parse_detail, dont_filter=True)  # 解析工作的招聘目录
                    request.meta['item'] = item  # 将item暂存
                    print(item)
                    yield request
                except Exception:
                    continue  # 继续循环
        except Exception:
            pass
        # 下一页
        try:
            next_page = response.xpath(".//*[@class='page_no']/@href").extract()  # 下一页链接
            current_page_index = int(response.xpath(".//*[@class='page_no pager_is_current']/@data-index").extract()[0])  # 当前页码
            next_page_index = int(response.xpath(".//*[@class='page_no']/@data-index").extract()[-1])  # 下一页的页码

            if next_page and next_page_index > current_page_index:
                    next_page_url = int(next_page[-1])
                    yield scrapy.Request(url=next_page_url, callback=self.parse)
        except Exception:
            pass

    def parse_detail(self, response):
        """
        解析具体的工作页面，提取工作描述
        :param response:
        :return:
        """
        try:
            job_detail = response.xpath(".//*[@class='job-detail']").xpath('string(.)').extract()[0]  # 职位描述
        except Exception:
            job_detail = ''  # 出错则赋值空
        # 重新构造item
        item = response.meta['item']
        job = item['job']  # 工作
        category = str(item['category']).strip()  # 工作主类别
        sub_category = item['sub_category']  # 子类
        job_url_menu = item['job_url_menu']  # 具体工作的招聘目录链接
        concrete_job = item['concrete_job']
        concrete_job_url = item['concrete_job_url']
        job_position = item['job_position']
        publish_time = item['publish_time']
        salary = item['salary']
        work_experience = str(item['work_experience']).strip()
        company_scale = str(item['company_scale']).strip()
        job_label = str(item['job_label']).replace('\n', '\t')
        company = item['company']
        company_welfare = item['company_welfare']
        item = LagouProjectItem(job=job, job_url_menu=job_url_menu,
                                category=category, sub_category=sub_category, concrete_job=concrete_job,
                                concrete_job_url=concrete_job_url, job_position=job_position,
                                publish_time=publish_time, salary=salary, work_experience=work_experience,
                                company=company, company_scale=company_scale, job_label=job_label,
                                company_welfare=company_welfare, job_detail=job_detail)
        yield item


