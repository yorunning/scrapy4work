from scrapy.selector import Selector

class FilterBrandMiddleware:
    def process_response(self,request,response,spider):
        selector = Selector(response)

        pass
