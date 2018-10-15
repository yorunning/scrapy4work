from scrapy import signals
from scrapy_splash import SplashRequest
import logging


class ProxyMiddleware:
    """设置代理"""

    def __init__(self, proxy):
        self.logger = logging.getLogger('work.middlewares.ProxyMiddleware')
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings.get('HTTP_PROXY'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if isinstance(request, SplashRequest):
            # SplashRequest
            request.meta['splash']['args']['proxy'] = f'http://{self.proxy}'
        # others
        request.meta['proxy'] = f'http://{self.proxy}'

    def spider_opened(self):
        self.logger.info('ProxyMiddleware opened')
