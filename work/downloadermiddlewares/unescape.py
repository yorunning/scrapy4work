import html
from scrapy.http import HtmlResponse


class HtmlUnEscapeMiddleware:
    """反转义HTML转义字符"""

    def process_response(self, response, request, spider):
        body_unescape = html.unescape(response.text)
        return HtmlResponse(url=response.url, body=body_unescape,
                            request=request, encoding='utf-8')
