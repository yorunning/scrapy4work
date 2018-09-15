# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from work.items import ShopItem
from scrapy_selenium import SeleniumRequest


class HuffashionsSpider(scrapy.Spider):
    name = 'huffashions'
    allowed_domains = ['www.huffashions.com']
    start_urls = ['http://www.huffashions.com/apparel-wholesale']
    custom_settings = {
        'MYSQL_TABLE': 'huffashions_table'
    }

    def parse(self, response):
        """
        解析一级导航链接
        :param response:
        :return:
        """
        nav_list = response.xpath('//ul[@id="left-navp"]//ul[@class="level0"]/li')

        for link in nav_list:
            url = link.xpath('./a/@href').extract_first()

            # yield Request(url, callback=self.parse_link_list2)
            yield SeleniumRequest(url=url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        """
        解析商品列表链接
        :param response:
        :return:
        """
        cat1 = response.xpath('//div[@class="breadcrumbs"]/ul/li[2]/a/text()').extract_first()
        cat2 = response.xpath('//div[@class="breadcrumbs"]/ul/li[3]/strong/text()').extract_first()

        product_list = response.xpath('//li[@class="item last"]')

        for link in product_list:
            url = link.xpath('./a/@href').extract_first()

            yield SeleniumRequest(url=url, callback=self.parse_item, meta={'cat1': cat1, 'cat2': cat2})

    def parse_item(self, response):
        """
        解析商品信息
        :param response:
        :return:
        """
        item = ShopItem()

        item['url'] = response.url
        item['brand'] = 'Huf'
        item['gender'] = ''
        item['producttype'] = response.meta['cat1']
        item['category'] = item['brand'] + '|||' + item['producttype'] + '|||' + response.meta['cat2']

        item['title'] = response.xpath('//span[@class="h1"]/text()').get()
        item['price'] = response.xpath('//div[@class="price-info"]//span[@class="price"]/text()')[
            1].get()
        item['short_content'] = response.xpath('//div[@class="std"]/node()')[-1].get().strip() or ''
        item['content'] = ''
        item['picture'] = '|||'.join(response.xpath('//div[@class="product-image-gallery"]/img/@src')[1:].getall())
        item['yanse'] = response.xpath('//div[@class="input-box"]')[1].xpath('.//option[2]/text()').get().strip()
        item['size'] = '|||'.join(
            [i.strip() for i in response.xpath('//div[@class="input-box"]')[2].xpath('.//option/text()')[1:].getall()])

        yield item
