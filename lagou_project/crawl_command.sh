#!/usr/bin/env bash
#scrapy crawl lagou_project  # 启动爬虫命令
#scrapy crawl lagou_project -o crawl_star.json
#scrapy crawl lagou_project_index -o crawl_star_index.json
scrapy crawl lagou_project_menu -o lagou_project_menu.json
#scrapy crawl lagou_project_job_detail -o lagou_project_job_detail.json
