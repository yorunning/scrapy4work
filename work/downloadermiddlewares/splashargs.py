from scrapy import signals
from scrapy_splash import SplashRequest
import logging


class SplashArgsMiddleware:
    """设置splash常用的参数"""

    def __init__(self):
        self.logger = logging.getLogger('work.SplashArgsMiddleware')

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if isinstance(request, SplashRequest):
            splash_args = request.meta['splash']['args']

            splash_args.setdefault('wait', 5)
            splash_args.setdefault('timeout', 60)
            splash_args.setdefault('resource_timeout', 10)
            splash_args.setdefault('images', 0)

    def spider_opened(self):
        self.logger.info('SplashArgsMiddleware opened')
