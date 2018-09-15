# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from work.items import ShopItem
import re


class A1906SoftmocSpider(scrapy.Spider):
    name = '1906_softmoc'
    allowed_domains = ['www.softmoc.com']
    start_urls = ['https://www.softmoc.com/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_1906',
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ul[@class="menu expanded"]/li')[1:6]

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get().strip()
            nav_level_2_list = list(nav_level_1.xpath('.//td[@class="menu-category"][2]'))

            for nav_level_2 in nav_level_2_list:
                # cat2 = nav_level_2.xpath('').get().strip()
                nav_level_3_list = nav_level_2.xpath('./a')

                for nav_level_3 in nav_level_3_list:
                    cat2 = nav_level_3.xpath('./text()').get().strip()
                    nav_level_3_url = nav_level_3.xpath('./@href').get()

                    print(f'{cat1}---{cat2}')

                    meta = {'cat1': cat1, 'cat2': cat2}

                    yield SplashRequest(response.urljoin(nav_level_3_url), self.parse_product_url, meta=meta,
                                        args={
                                            'wait': 2,
                                            'timeout': 300,
                                            'images_enabled': 0,
                                        })

    def parse_product_url(self, response):
        product_list = response.xpath('//div[@class="column text-center grid-item"]')

        for product in product_list:
            product_url = product.xpath('.//div[@class="reg-view"]/a/@href').get()

            yield SplashRequest(response.urljoin(product_url), self.parse_product_info, meta=response.meta,
                                args={
                                    'wait': 2,
                                    'timeout': 300,
                                    'images_enabled': 0,
                                })

        next_page = response.xpath('').get()

        if next_page is not None:
            yield SplashRequest(response.urljoin(next_page), self.parse_product_url, meta=response.meta,
                                args={
                                    'wait': 2,
                                    'timeout': 300,
                                    'images_enabled': 0,
                                })

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']

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
