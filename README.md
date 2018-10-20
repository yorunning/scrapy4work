
## 内容提取规范

+ 确定是单个值使用get()
+ 可能存在多个值的一律使用getall()
+ 值不能为NoneType，需使用空字符串''替换None

## downloader middlewares

|中间件|所在模块|作用|
|---|---|---|
|ProxyMiddleware       |proxy.py     |设置代理|
|SplashArgsMiddleware  |splashargs.py|设置splash常用的参数|
|HtmlUnEscapeMiddleware|unescape.py  |反转义HTML转义字符|

## spider middlewares

|中间件|所在模块|作用|
|---|---|---|
|StripAllMiddleware          |strip.py  |去除内容前后空白|
|SpliceCategoryMiddleware    |splice.py |拼接category|
|SpliceListMiddleware        |splice.py |拼接列表字段|
|GenerateSkuMiddleware       |genku.py  |生成sku及库存|
|ProcessSpecialCharMiddleware|special.py|处理特殊字符|

## pipelines

|管道|所在模块|作用|
|---|---|---|
|FilterBrandPipeline|pipelines.py|过滤违禁品|
|MysqlPipeline      |pipelines.py|数据存放到mysql数据库|
|AioMysqlPipeline   |pipelines.py|mysql异步支持|

## resource

数据库所需的信息

add `db_info.json` to `～/resource`

```json
{
  "host": "host",
  "user": "username",
  "password": "password",
  "database": "database"
}
```

代理相关

add `proxy.json` to `～/resource`

```json
{
  "proxy_url": "ip:port",
  "splash_url": "ip:8050"
}
```

违禁品清单  
disallow_brand.txt