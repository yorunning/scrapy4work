from work.items import ShopItem


class SpliceCategoryMiddleware:
    """ 拼接category"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                if r.get('cat4', False):
                    r['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3'], r['cat4']))
                elif r.get('cat3', False):
                    r['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3']))
                elif r.get('cat2', False):
                    r['category'] = '|||'.join((r['cat1'], r['cat2']))
                else:
                    r['category'] = r['cat1']

                yield r
