# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopItem(scrapy.Item):
    """
    单个值使用get(), 可能存在多个值的一律使用getall()
    quick use:
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']

        item['brand'] =
        item['gender'] =
        item['producttype'] =

        item['title'] = response.xpath('')
        item['price'] = response.xpath('')
        item['short_content'] = response.xpath('')
        item['content'] = response.xpath('')
        item['pictures'] = response.xpath('')
        item['color'] = response.xpath('')
        item['size'] = response.xpath('')
    """

    # custom field
    cat1 = scrapy.Field()
    cat2 = scrapy.Field()
    cat3 = scrapy.Field()
    cat4 = scrapy.Field()

    # category info
    brand = scrapy.Field()
    gender = scrapy.Field()
    producttype = scrapy.Field()
    category = scrapy.Field()

    # product info
    title = scrapy.Field()
    price = scrapy.Field()
    short_content = scrapy.Field()
    content = scrapy.Field()
    pictures = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()

    # other field
    PageUrl = scrapy.Field()
    prosku = scrapy.Field()
    stock = scrapy.Field()

    # caturlsuf = scrapy.Field()
    # description = scrapy.Field()
    # ratio = scrapy.Field()
    # clearWords = scrapy.Field()
    # designers = scrapy.Field()
    # filters = scrapy.Field()
