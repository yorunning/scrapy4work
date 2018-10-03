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
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
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
    'work.spidermiddlewares.generatesku.GenerateSkuMiddleware': 902,
    'work.spidermiddlewares.processspecialchar.ProcessSpecialCharMiddleware': 901,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

    # 'scrapy_selenium.SeleniumMiddleware': 800,

    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,

    # 'work.downloadermiddlewares.selenium.SeleniumMiddleware': 800,
    'work.downloadermiddlewares.splashargs.SplashArgsMiddleware': 730,
    'work.downloadermiddlewares.proxy.ProxyMiddleware': 740,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
# }


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'work.pipelines.MysqlPipeline': None,
    'work.pipelines.AioMysqlPipeline': None,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


""" custom sittings"""

dir_path = path.abspath('./work/json')

# 加载代理json
proxy_path = path.join(dir_path, 'proxy.json')
proxy = json.load(open(proxy_path))

HTTP_PROXY = proxy.get('http_proxy')
splash_url = proxy.get('splash_url')

# selenium required
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
# SELENIUM_DRIVER_ARGUMENTS = []
# TIMEOUT = 10

# splash required
SPLASH_URL = f'http://{splash_url}'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 加载数据库信息
db_info_path = path.join(dir_path, 'db_info.json')
db_info = json.load(open(db_info_path))

MYSQL_HOST = db_info.get('host')
MYSQL_USER = db_info.get('user')
MYSQL_PASSWORD = db_info.get('password')
MYSQL_DATABASE = db_info.get('database')
MYSQL_TABLE = None  # defined in spider.py
