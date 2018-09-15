# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from work.items import ShopItem
import re


class SierratradingpostSpider(scrapy.Spider):
    name = 'sierratradingpost'
    allowed_domains = ['www.sierratradingpost.com']
    start_urls = ['https://www.sierratradingpost.com/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_1864',
        # 'ITEM_PIPELINES': {
        #     'work.pipelines.MysqlPipeline': None
        # }
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//div[contains(@class,"nav-item dropdown navigation-dropdown")]')[1:5]

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').extract_first().strip()
            nav_level_2_list = nav_level_1.xpath('./div/div[2]/div')

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2.xpath('./a/text()').get().strip()
                nav_level_3_list = nav_level_2.xpath('./div/a')[2:]

                for nav_level_3 in nav_level_3_list:
                    cat3 = nav_level_3.xpath('./text()').get().strip()
                    nav_level_3_url = nav_level_3.xpath('./@href').get()

                    print(f'{cat1}---{cat2}---{cat3}')

                    meta = {'cat1': cat1, 'cat2': cat2, 'cat3': cat3}
                    yield Request(response.urljoin(nav_level_3_url), callback=self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//div[contains(@class,"productThumbnailContainer")]')

        for product in product_list:
            url = product.xpath('./div/a/@href').get()

            yield Request(response.urljoin(url), callback=self.parse_product_info, meta=response.meta)

        next_page = response.xpath('//link[@rel="next"]/@href').get()

        yield Request(response.urljoin(next_page), callback=self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']
        item['category'] = '|||'.join((item['cat1'], item['cat2'], item['cat3']))

        item['brand'] = response.xpath('//h1[@itemprop="name"]/a/text()').get()
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = ''.join(response.xpath('//h1[@itemprop="name"]/text()').getall())
        item['price'] = response.xpath('//meta[@name="product:price:amount"]/@content').get()
        item['short_content'] = ''

        content = response.xpath('//ul[@class="list m-t-sm links-underline"]').get()
        item['content'] = re.sub(r'<a.*?</a>', '', content)

        picture = response.xpath('//input[@id="largeImageSrcTemplate"]/@value').get()
        pictures = '|||'.join(response.xpath('//div[@data-ajaxaltimage-next-index]/a/@href').getall())
        item['pictures'] = pictures or picture
        item['color'] = response.xpath('//select[@id="selectedProperty1"]/option[2]/text()').get()
        item['size'] = '|||'.join(response.xpath('//select[@id="selectedProperty2"]/option/text()')[1:].getall())

        yield item