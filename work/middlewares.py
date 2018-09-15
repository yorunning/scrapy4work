# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from work.items import ShopItem
import random
import re
from scrapy_splash import SplashRequest


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TutorialDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware:
    """
    downloaderMiddleware
    使用selenium渲染html
    """

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

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self):
        self.driver.close()


class ProxyMiddleware:
    """
    downloaderMiddleware
    设置代理
    """

    def process_request(self, request, spider):
        if isinstance(request, SplashRequest):
            # SplashRequest
            request.meta['splash']['args']['proxy'] = 'http://10.0.0.59:1080'
        else:
            # scrapy Request and SeleniumRequest
            request.meta['proxy'] = 'http://127.0.0.1:1080'


class CommonFilterMiddleware:
    """
    spiderMiddleware
    对数据处理进行一些常用的处理
    """

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                item = r.copy()

                # 拼接category
                if item.get('cat4', False):
                    item['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3'], r['cat4']))
                elif item.get('cat3', False):
                    item['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3']))
                else:
                    item['category'] = '|||'.join((r['cat1'], r['cat2']))

                # 去头部尾部空格、join list
                item['title'] = r['title'].strip()
                item['price'] = r['price'].strip().strip('$').strip('£').strip('€')
                item['short_content'] = r['short_content'].strip() if r['short_content'] is not None else ''
                item['content'] = r['content'].strip() if r['content'] is not None else ''

                item['pictures'] = '|||'.join(r['pictures'])
                item['color'] = '|||'.join(r['color'])
                item['size'] = '|||'.join([size.strip() for size in r['size']])

                # 给其他字段赋值
                color = r['color'].split('|||')[0]
                random_num = str(random.randint(1, 999999))

                sku = '_'.join((r['brand'], r['gender'], r['producttype'], color, random_num)).strip().strip('_')
                sku = re.sub(r'[\s&/__]+', '_', sku)

                item['prosku'] = sku
                item['stock'] = '999'

                yield item
