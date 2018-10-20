# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from work.items import ShopItem
import re


class Test2Spider(scrapy.Spider):
    name = 'test2'
    allowed_domains = ['www.countryattire.com']
    start_urls = ['https://www.countryattire.com/']

    custom_settings = {
        'MYSQL_TABLE': 'test',
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        nav = response.xpath('//ul[@id="pronav"]/li')[2:8]
        nav.pop(3)
        nav_level_1_list = nav

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/span/text()').get().strip()
            nav_level_2_list = nav_level_1.xpath('.//div[@id="menu"]/div')[1:]

            for nav_level_2 in nav_level_2_list:
                c2 = nav_level_2.xpath('./div/div/span/text()').get()
                if c2 is None:
                    c2 = nav_level_2.xpath('./div/div/span/a/text()').get()
                    if c2 is None:
                        c2 = nav_level_2.xpath('./div/div/span/span/text()').get()
                cat2 = c2.strip()

                nav_level_3_list = nav_level_2.xpath('./div/span')

                if not nav_level_3_list:
                    nav_level_2_url = nav_level_2.xpath('./a/@href').get()

                    self.logger.info(f'{cat1}---{cat2}')
                    meta = {'cat1': cat1, 'cat2': cat2}

                    yield SplashRequest(response.urljoin(nav_level_2_url), self.parse_product_url, meta=meta)

                for nav_level_3 in nav_level_3_list:
                    cat3 = nav_level_3.xpath('./a/text()').get().strip()
                    nav_level_3_url = nav_level_3.xpath('./a/@href').get()

                    self.logger.info(f'{cat1}---{cat2}---{cat3}')
                    meta = {'cat1': cat1, 'cat2': cat2, 'cat3': cat3}

                    yield SplashRequest(response.urljoin(nav_level_3_url), self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//div[@class="products-grid"]/div')

        for product in product_list:
            product_url = product.xpath('./a/@href').get()

            self.logger.info('product url is %s' % product_url)

            # yield SplashRequest(response.urljoin(product_url), self.parse_product_info, meta=response.meta)

        next_page = response.xpath('//a[@class="next i-next"]/@href').get()

        # self.logger.info('next page is %s' % next_page)

        if next_page is not None:
            yield SplashRequest(response.urljoin(next_page), self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3'] or ''

        item['brand'] = response.xpath('').get().strip()
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('').get()
        item['price'] = response.xpath('').get()
        item['short_content'] = ''
        item['content'] = response.xpath('').get()

        pictures = response.xpath('').getall()
        picture = response.xpath('').getall()
        item['pictures'] = pictures or picture

        item['color'] = ''
        item['size'] = response.xpath('').getall()

        yield item
