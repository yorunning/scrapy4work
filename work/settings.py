# -*- coding: utf-8 -*-

from shutil import which
from os import path
import json

BOT_NAME = 'work'

SPIDER_MODULES = ['work.spiders']
NEWSPIDER_MODULE = 'work.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,

    'work.spidermiddlewares.strip.StripAllMiddleware': 905,
    'work.spidermiddlewares.splice.SpliceCategoryMiddleware': 904,
    'work.spidermiddlewares.splice.SpliceListMiddleware': 903,
    'work.spidermiddlewares.gensku.GenerateSkuMiddleware': 902,
    'work.spidermiddlewares.special.ProcessSpecialCharMiddleware': 901,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 随机UA
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

    # splash渲染
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,

    # selenium渲染
    # 'scrapy_selenium.SeleniumMiddleware': 800,

    # 'work.downloadermiddlewares.selenium.SeleniumMiddleware': 800,
    'work.downloadermiddlewares.splashargs.SplashArgsMiddleware': 730,
    'work.downloadermiddlewares.proxy.ProxyMiddleware': 740,

    'work.downloadermiddlewares.unescape.HtmlUnEscapeMiddleware': 200
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'work.pipelines.FilterBrandPipeline': 90,
    'work.pipelines.MysqlPipeline': None,
    'work.pipelines.AioMysqlPipeline': None,
}

# 资源文件夹路径
resource_path = path.abspath('./work/resource')

# 违禁品路径
DISALLOW_BRAND = path.join(resource_path, 'disallow_brand.txt')

# 加载数据库信息
db_info_path = path.join(resource_path, 'db_info.json')
db_info = json.load(open(db_info_path))

MYSQL_HOST = db_info.get('host')
MYSQL_USER = db_info.get('user')
MYSQL_PASSWORD = db_info.get('password')
MYSQL_DATABASE = db_info.get('database')
MYSQL_TABLE = None  # defined in spider.py

# 加载代理
proxy_path = path.join(resource_path, 'proxy.json')
proxy = json.load(open(proxy_path))

# http代理
HTTP_PROXY = proxy.get('proxy_url')

# splash required
SPLASH_URL = 'http://{}'.format(proxy.get('splash_url'))
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# selenium required
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
# SELENIUM_DRIVER_ARGUMENTS = []

FAKEUSERAGENT_FALLBACK = 'Mozilla'