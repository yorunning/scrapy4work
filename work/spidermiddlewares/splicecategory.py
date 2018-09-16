from work.items import ShopItem


class SpliceCategoryMiddleware:
    """ 拼接category
    """

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                item = r.copy()

                if r.get('cat4', False):
                    item['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3'], r['cat4']))
                elif r.get('cat3', False):
                    item['category'] = '|||'.join((r['cat1'], r['cat2'], r['cat3']))
                else:
                    item['category'] = '|||'.join((r['cat1'], r['cat2']))

                yield item
