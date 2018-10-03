from work.items import ShopItem


class StripAllMiddleware:
    """ 去内容前后空白"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                r['cat1'] = r['cat1'].strip() if r.get('cat1') else ''
                r['cat2'] = r['cat2'].strip() if r.get('cat2') else ''
                r['cat3'] = r['cat3'].strip() if r.get('cat3') else ''
                r['cat4'] = r['cat4'].strip() if r.get('cat4') else ''

                r['brand'] = r['brand'].strip()
                r['gender'] = r['gender'].strip()
                r['producttype'] = r['producttype'].strip()

                r['title'] = r['title'].strip()
                r['price'] = r['price'].strip()
                r['short_content'] = r['short_content'].strip()
                r['content'] = r['content'].strip()

                # r['pictures'] = [p.strip() for p in r['pictures']]
                r['color'] = [c.strip() for c in r['color']]
                r['size'] = [s.strip() for s in r['size']]

                yield r
