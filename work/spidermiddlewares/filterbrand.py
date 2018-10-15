from work.items import ShopItem
from work.utils import filter_brand

class FilterBrandMiddleware:
    """过滤违禁品"""
    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                if filter_brand(r['brand']):
                    pass
