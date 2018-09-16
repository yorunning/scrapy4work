# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from work.items import ShopItem
from scrapy_selenium import SeleniumRequest


class HuffashionsSpider(scrapy.Spider):
    """
    主要用于测试scrapy框架的整合
    """
    name = 'huffashions'
    allowed_domains = ['www.huffashions.com']
    start_urls = ['http://www.huffashions.com/']
    custom_settings = {
        'MYSQL_TABLE': 'huffashions_table',
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ol[@class="nav-primary"]/li')

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get()
            nav_level_2_list = nav_level_1.xpath('./ul/li')[1:]

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2.xpath('./a/text()').get()
                nav_level_2_url = nav_level_2.xpath('./@href').get()

                print(f'{cat1}---{cat2}')

                meta = {
                    'cat1': cat1,
                    'cat2': cat2
                }

                yield Request(response.urljoin(nav_level_2_url), self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//li[@class="item last"]')

        for product in product_list:
            product_url = product.xpath('./a/@href').get()
            yield Request(response.urljoin(product_url), self.parse_product_info, meta=response.meta)

        next_page = response.xpath('//a[@class="next i-next"]/@href').get()

        if next_page is not None:
            yield Request(response.urljoin(next_page), self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']

        item['brand'] = 'Huf'
        item['gender'] = 'Men'
        item['producttype'] = item['cat1']

        item['title'] = response.xpath('//span[@class="h1"]/text()').get()
        item['price'] = response.xpath('//div[@class="price-box"]/p[last()]/span[@class="price"]/text()').get()

        item['short_content'] = ''
        item['content'] = response.xpath('//div[@class="std"]').get()

        pictures = response.xpath('//img[@class="gallery-image"]/@src').getall()
        item['pictures'] = pictures

        item['color'] = response.xpath(
            '//label[@class="required"][contains(text(),"Color")]/following::select[1]/option/text()')[1:].getall()

        item['size'] = response.xpath(
            '//label[@class="required"][contains(text(),"Size")]/following::select[1]/option/text()')[1:].getall()

        yield item
