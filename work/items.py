# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ShopItem(Item):
    """
    单个值使用get()，可能存在多个值的一律使用getall()
    值不能为NoneType，使用空字符串''替换

    quick use:
        item = ShopItem()

        item['PageUrl'] = response.url
        item['cat1'] = response.meta['cat1']
        item['cat2'] = response.meta['cat2']
        item['cat3'] = response.meta['cat3']

        item['brand'] = response.xpath('')
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
    cat1 = Field()
    cat2 = Field()
    cat3 = Field()
    cat4 = Field()

    # category info
    category = Field()
    brand = Field()
    gender = Field()
    producttype = Field()

    # product info
    title = Field()
    price = Field()
    short_content = Field()
    content = Field()
    pictures = Field()
    color = Field()
    size = Field()

    # other field
    prosku = Field()
    stock = Field()
    PageUrl = Field()

    # caturlsuf = scrapy.Field()
    # description = scrapy.Field()
    # ratio = scrapy.Field()
    # clearWords = scrapy.Field()
    # designers = scrapy.Field()
    # filters = scrapy.Field()
