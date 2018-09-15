# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from work.items import ShopItem


class A1866QuarkshoesSpider(scrapy.Spider):
    name = '1866_quarkshoes'
    allowed_domains = ['www.quarkshoes.com']
    start_urls = ['https://www.quarkshoes.com/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_1866',
        # 'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        nav_level_1_list = response.xpath('//ul[@class="cms-mega-menu"]/li')[:3]

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./span/a/text()').get().strip()
            nav_level_2_list = nav_level_1.xpath('./ul/li')

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2_list[0].xpath('.//h2/a/text()').get().strip()
                nav_level_3_list = nav_level_2.xpath('.//ul/li')[:-1]

                for nav_level_3 in nav_level_3_list:
                    cat3 = nav_level_3.xpath('./a/text()').get().strip()
                    nav_level_3_url = nav_level_3.xpath('./a/@href').get()

                    print(f'{cat1}---{cat2}---{cat3}')

                    meta = {'cat1': cat1, 'cat2': cat2, 'cat3': cat3}
                    yield Request(response.urljoin(nav_level_3_url), callback=self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//div[contains(@class,"product-tile")]')

        for product in product_list:
            product_url = product.xpath('./a/@href').get()

            yield Request(response.urljoin(product_url), self.parse_product_info, meta=response.meta)

        next_page = response.xpath('//div[@class="pager pager-top"]//li[last()]/a/@href').get()
        if next_page is not None:
            yield Request(response.urljoin(next_page), self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']
        item['category'] = '|||'.join((item['cat1'], item['cat2'], item['cat3']))

        item['brand'] = response.xpath('//hgroup[@class="product-title"]/h2/text()').get()
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('.').re(r'"price": "(.*?)"')[0]
        item['short_content'] = ''
        item['content'] = response.xpath('//meta[@name="description"]/@content').get()

        pictures = '|||'.join([response.urljoin(p)
                               for p in
                               response.xpath('//ul[contains(@id,"product-secondary-images")]/li//a/@href').getall()])

        picture = response.urljoin(response.xpath('//section[@class="images"]/div/a[1]/img/@href').get())
        item['pictures'] = pictures or picture

        item['color'] = ''
        item['size'] = '|||'.join(response.xpath('//select[@class="size "]/option/text()').getall())

        yield item
