from scrapy_splash import SplashRequest


class ProxyMiddleware:
    """ 设置代理"""

    def __init__(self, proxy):
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings.get('HTTP_PROXY'))
        return s

    def process_request(self, request, spider):
        if isinstance(request, SplashRequest):
            # SplashRequest
            request.meta['splash']['args']['proxy'] = f'http://{self.proxy}'
        else:
            # scrapy Request and SeleniumRequest
            request.meta['proxy'] = f'http://{self.proxy}'
