# -*- coding: utf-8 -*-

# Scrapy settings for crawl_star_image_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
"""
设置log
"""
# 设置数据的输出编码
FEED_EXPORT_ENCODING = 'utf-8'

# 设置log
LOG_FILE = './crawl_stars.log'  # log位置
LOG_LEVEL = 'WARNING'  # 输出等级
"""
Scrapy提供5层logging级别:

CRITICAL - 严重错误

ERROR - 一般错误

WARNING - 警告信息

INFO - 一般信息

DEBUG - 调试信息
"""


BOT_NAME = 'crawl_star_image_project'

SPIDER_MODULES = ['crawl_star_image_project.spiders']
NEWSPIDER_MODULE = 'crawl_star_image_project.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_star_image_project (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawl_star_image_project.middlewares.CrawlStarImageProjectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawl_star_image_project.middlewares.CrawlStarImageProjectDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
图片/文件下载
"""
ITEM_PIPELINES = {
   'crawl_star_image_project.pipelines.CrawlStarImageProjectPipeline': 300,
   'scrapy.pipelines.images.ImagesPipeline': 1  # 图片下载
   # 'scrapy.pipelines.files.FilesPipeline': 1  # 文件下载

}
IMAGES_STORE = 'image'  # 存储路径
IMAGES_URLS_FIELD = 'images_url'  # 图片URL在items.py的字段
IMAGES_RESULT_FIELD = 'image'  # 图片结果信息在items.py的字段

# 设置缩略图大小
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270)
}
IMAGES_EXPIRES = 30  # 30天后过期

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
