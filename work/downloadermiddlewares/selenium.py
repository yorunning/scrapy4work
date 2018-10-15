from scrapy import signals
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging


class SeleniumMiddleware:
    """使用selenium渲染html"""

    def __init__(self, timeout):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(timeout)
        self.wait = WebDriverWait(self.driver, timeout)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings.get('TIMEOUT'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, request=request,
                            encoding='utf-8', status=200)

    def spider_opened(self):
        logger = logging.getLogger('work.middleware.SeleniumMiddleware')
        logger.info('SeleniumMiddleware opened')

    def spider_closed(self):
        self.driver.quit()
