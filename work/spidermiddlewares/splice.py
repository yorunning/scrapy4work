from work.items import ShopItem


class SpliceCategoryMiddleware:
    """拼接category"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                if not r.get('cat4') == '':
                    r['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3'], r['cat4']))
                elif r.get('cat3'):
                    r['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3']))
                elif r.get('cat2'):
                    r['category'] = '|||'.join((r['cat1'], r['cat2']))
                else:
                    r['category'] = r['cat1']

                yield r


class SpliceListMiddleware:
    """拼接列表字段"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                r['pictures'] = '|||'.join(r['pictures'])
                r['color'] = '|||'.join(r['color'])
                r['size'] = '|||'.join(r['size'])

                yield r
