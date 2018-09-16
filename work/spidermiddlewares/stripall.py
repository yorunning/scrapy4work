from work.items import ShopItem


class StripAllMiddleware:

    def process_spider_output(self, response, result, request):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                item = r.copy()

                item['cat1'] = r['cat1'].strip() if r.get('cat1') else None
                item['cat2'] = r['cat2'].strip() if r.get('cat2') else None
                item['cat3'] = r['cat3'].strip() if r.get('cat3') else None
                item['cat4'] = r['cat4'].strip() if r.get('cat4') else None

                item['brand'] = r['brand'].strip()
                item['gender'] = r['gender'].strip()
                item['producttype'] = r['producttype'].strip()

                item['title'] = r['title'].strip()
                item['price'] = r['price'].strip()
                item['short_content'] = r['short_content'].strip()
                item['content'] = r['content'].strip()

                # item['pictures'] = [p.strip() for p in r['pictures']]
                item['color'] = [c.strip() for c in r['color']]
                item['size'] = [s.strip() for s in r['size']]

                yield item
