from work.items import ShopItem
import re


class ProcessSpecialCharMiddleware:
    """ 处理特殊字符"""

    def process_spider_output(self, response, result, spider):
        for r in result:
            if not isinstance(r, ShopItem):
                yield r
            else:
                # 去掉价格符号
                r['price'] = r['price'].strip('$').strip('£').strip('€')

                # 替换 &#309; 为 ’
                r['title'] = re.sub(r'&#309;', '\'', r['title'])

                yield r
