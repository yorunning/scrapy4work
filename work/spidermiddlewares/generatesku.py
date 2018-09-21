from work.items import ShopItem
import random, re


class GenerateSkuMiddleware:
    """ 生成sku及库存"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                color = r['color'].split('|||')[0]
                random_num = str(random.randint(1, 999999))

                sku = '_'.join((r['brand'], r['gender'], r['producttype'], color, random_num)) # 拼接

                sku = sku.strip('_') # 去掉头部可能出现的_
                sku = re.sub(r'[\s&/_]+', '_', sku) # 替换特殊字符

                r['prosku'] = sku
                r['stock'] = '999'

                yield r
