# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from work.items import ShopItem
import re
from scrapy_splash import SplashRequest



class A1865NevisportSpider(scrapy.Spider):
    name = '1865_nevisport'
    allowed_domains = ['www.nevisport.com']
    start_urls = ['https://www.nevisport.com/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_1865',
        'CONCURRENT_REQUESTS': 4,
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ul[@class="main_menu clean hard"]/li')[:4]

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get().strip()
            nav_level_2_url = nav_level_1.xpath('./a/@href').get()

            yield Request(nav_level_2_url, callback=self.parse_nav_level_2, meta={'cat1': cat1})

    def parse_nav_level_2(self, response):
        nav_level_2_list = response.xpath('//div[@class="grid blocks cat-items"]/div')

        for nav_level_2 in nav_level_2_list:
            cat2 = nav_level_2.xpath('./a//p/text()').get().strip()
            nav_level_3_url = nav_level_2.xpath('./a/@href').get()

            meta = response.meta
            meta['cat2'] = cat2

            yield Request(nav_level_3_url, self.parse_nav_level_3, meta=meta)

    def parse_nav_level_3(self, response):
        nav_level_3_list = response.xpath('//div[@class="grid blocks cat-items"]/div')

        for nav_level_3 in nav_level_3_list:
            cat3 = nav_level_3.xpath('./a//p/text()').get().strip()
            nav_level_4_url = nav_level_3.xpath('./a/@href').get()

            meta = response.meta
            meta['cat3'] = cat3

            yield Request(nav_level_4_url, self.parse_nav_level_4, meta=meta)

    def parse_nav_level_4(self, response):
        nav_level_4_list = response.xpath('//div[@class="grid blocks cat-items"]/div')

        for nav_level_4 in nav_level_4_list:
            cat4 = nav_level_4.xpath('./a//p/text()').get().strip()
            product_list_url = nav_level_4.xpath('./a/@href').get()

            meta = response.meta
            meta['cat4'] = cat4

            print(f'{meta["cat1"]}---{meta["cat2"]}---{meta["cat3"]}---{meta["cat4"]}')

            yield Request(product_list_url, self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//div[@class="product__image"]')

        for product in product_list:
            product_url = product.xpath('./a/@href').get()

            yield SplashRequest(product_url, self.parse_product_info, meta=response.meta,args={'wait':3,'proxy':'http://10.0.0.59:1080'})

        next_page = response.xpath('//link[@rel="next"]/@href').get()

        if next_page is not None:
            yield Request(next_page, self.parse_product_url,meta=response.meta)

    def parse_product_info(self, response):

        # print(response.body)

        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']
        item['cat4'] = response.meta['cat4']
        item['category'] = '|||'.join((item['cat1'], item['cat2'], item['cat3'], item['cat4']))

        item['brand'] = ''
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//span[@class="price"]/text()').get()
        item['short_content'] = ''

        content = response.xpath('//article').get()
        content = re.sub(r'<div class="additional">(.|\n)*?</div>', '', content)
        item['content'] = content

        item['color'] = response.xpath('//div[@id="attr_col"]//div[@class="col"]/label/@data-colour-name').get()
        item['size'] = '|||'.join(response.xpath('//dl[@id="attr_sizes"]//dd')[1:].xpath('./label/text()').getall())

        item['pictures'] = response.xpath('//div[@class="product_img--cont"]/img/@src').get()

        yield item
