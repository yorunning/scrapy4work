from work.items import ShopItem


class SpliceListMiddleware:
    """ 拼接列表字段"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                r['pictures'] = '|||'.join(r['pictures'])
                r['color'] = '|||'.join(r['color'])
                r['size'] = '|||'.join(r['size'])

                yield r
