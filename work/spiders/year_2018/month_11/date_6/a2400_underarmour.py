import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from work.items import ShopItem
import re


class A2400UnderarmourSpider(scrapy.Spider):
    """
    :# 语言: en
    :# 货币: url
    :# 主题: 单品 underarmour
    :# 备注: 检查数据
    """

    name = '2400_underarmour'
    allowed_domains = ['www.underarmour.com']
    start_urls = ['https://www.underarmour.com/en-us/']

    custom_settings = {
        'MYSQL_TABLE': 'data_content_2400',
        'ITEM_PIPELINES': {
            'work.pipelines.MysqlPipeline': 100,
            'work.pipelines.AioMysqlPipeline': None,
        }
    }

    def parse(self, response):
        nav_level_1_list = response.xpath(
            '//ul[@class="nav-list nav-list--categories"]/li[@class="ua-top-nav-category"]')
        nav_level_1_list.pop(5)

        for nav_level_1 in nav_level_1_list:
            cat1 = nav_level_1.xpath('./a/text()').get().strip()
            nav_level_2_list = nav_level_1.xpath('.//div[@class="nav-column default "]/ul/li')

            for nav_level_2 in nav_level_2_list:
                cat2 = nav_level_2.xpath('./a/text()').get().strip()
                nav_level_3_list = nav_level_2.xpath('./div/ul/li[@class="nav-list-item"]')

                for nav_level_3 in nav_level_3_list:
                    cat3 = nav_level_3.xpath('./a/text()').get().strip()
                    nav_level_3_url = nav_level_3.xpath('./a/@href').get()

                    self.logger.info(f'{cat1}---{cat2}---{cat3}')
                    meta = {'cat1': cat1, 'cat2': cat2, 'cat3': cat3}
                    # print(response.urljoin(nav_level_3_url))

                    yield Request(response.urljoin(nav_level_3_url), self.parse_product_url, meta=meta)

    def parse_product_url(self, response):
        product_list = response.xpath('//ul[@class="tileset stack-0"]/li')

        for product in product_list:
            product_url = product.xpath('.//a[@class="product-img-link"]/@href').get()

            yield Request(response.urljoin(product_url), self.parse_product_info, meta=response.meta)

        # next_page = response.xpath('').get()

        # if next_page is not None:
        #     yield Request(response.urljoin(next_page), self.parse_product_url, meta=response.meta)

    def parse_product_info(self, response):
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']

        item['brand'] = 'underarmour'
        item['gender'] = item['cat1']
        item['producttype'] = item['cat2']

        item['title'] = response.xpath('string(//h1)').get()
        item['price'] = response.xpath('//meta[@itemprop="price"]/@content').get()
        item['short_content'] = ''

        # content = response.xpath('.').re_first('"bullets":\["(.*)"\]')
        # content = re.sub(r'","', r'<br>', content)
        item['content'] = ''

        # pictures = response.xpath('').getall()
        picture = response.xpath('.').re('"imageUrl":"(.*)"')

        print(picture)
        item['pictures'] = list(picture)

        item['color'] = response.xpath('//span[@class="current-color-selection"]/text()').getall()
        item['size'] = response.xpath('//ul[@class="buypanel_sizelist"]/li/text()').getall()

        yield item
