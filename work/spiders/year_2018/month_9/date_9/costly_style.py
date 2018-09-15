# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from work.items import ShopItem


class CostlyStyleSpider(scrapy.Spider):
    name = 'costly_style'
    allowed_domains = ['www.costly-style.com']
    start_urls = ['http://www.costly-style.com/']

    custom_settings = {
        'MYSQL_TABLE': 'costly_style'
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ol[@class="nav-primary"]/li')

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get()
            nav_level_2_list = nav_level_1.xpath('./ul/li')[1:]

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2.xpath('./a/text()').get()
                nav_level_3_list = nav_level_2.xpath('./ul/li')[1:]

                for nav_level_3 in nav_level_3_list:
                    cat3 = nav_level_3.xpath('./a/text()').get()
                    nav_level_3_url = nav_level_3.xpath('./a/@href').get()

                    print(f'{cat1}---{cat2}---{cat3}')

                    yield Request(nav_level_3_url, callback=self.parse_product_url,
                                  meta={'cat1': cat1, 'cat2': cat2, 'cat3': cat3})

    def parse_product_url(self, response):
        # js
        product_list = response.xpath('//ul[@class="products-grid products-grid--max-3-col"]/li')

        for product in product_list:
            url = product.xpath('./a/@href').get()

            yield Request(url, callback=self.parse_product_info, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']
        item['category'] = '|||'.join((item['cat1'], item['cat2'], item['cat3']))

        # item['brand'] = ''
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('//span[@class="h1"]/text()').get()
        item['price'] = response.xpath('//span[@class="price"]/text()').get()
        item['short_content'] = ''
        item['content'] = response.xpath('//div[@class="std"]').get()
        item['pictures'] = '|||'.join(response.xpath('//div[@class="product-image-gallery"]/img/@src')[1:].getall())

        item['color'] = '|||'.join(
            response.xpath(
                '//label[@class="required"][contains(text(),"Color")]/following::select[1]/option/text()'
            )[1:].getall())

        item['size'] = '|||'.join(
            response.xpath(
                '//label[@class="required"][contains(text(),"Size")]/following::select[1]/option/text()'
            )[1:].getall())

        yield item
