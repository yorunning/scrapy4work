# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from work.items import ShopItem
import re


class A1906FramesfootwearSpider(scrapy.Spider):
    name = '1906_framesfootwear'
    allowed_domains = ['framesfootwear.co.nz']
    start_urls = ['https://framesfootwear.co.nz/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_1906',
        # 'ITEM_PIPELINES': {},
        'DOWNLOAD_DELAY': 10
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ul[@id="SiteNav"]/li')[:3]

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get().strip()
            nav_level_2_list = nav_level_1.xpath('.//div[@class="site-nav__childlist-item"]')

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2.xpath('./a/text()').get().strip()
                nav_level_2_url = nav_level_2.xpath('./a/@href').get()

                print(f'{cat1}---{cat2}')

                meta = {'cat1': cat1, 'cat2': cat2}

                yield Request(response.urljoin(nav_level_2_url), self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//div[@class="grid-view-item"]')

        for product in product_list:
            product_url = product.xpath('./a/@href').get()

            yield Request(response.urljoin(product_url), self.parse_product_info, meta=response.meta)

        next_page = response.xpath('//link[@rel="next"]/@href').get()

        if next_page is not None:
            yield Request(response.urljoin(next_page), self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']

        item['brand'] = response.xpath('.').re_first(r'"brand":"(.*?)"')
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('.').re_first(r'"price":"(.*?)"')
        item['short_content'] = response.xpath('//div[@itemprop="description"]/p/text()').get()
        item['content'] = response.xpath('//div[@itemprop="description"]/ul').get()

        pictures = response.xpath(
            '//li[@class="grid__item medium-up--one-quarter product-single__thumbnails-item js"]/a/@href').getall()
        pictures = ['https:' + p for p in pictures]
        picture = response.xpath('//div[@class="product-single__photo js-zoom-enabled"]/@data-zoom').getall()
        picture = ['https:' + p for p in picture]
        item['pictures'] = pictures or picture

        item['color'] = ''
        item['size'] = response.xpath('//select[@name="id"]/option/text()').getall()

        yield item
