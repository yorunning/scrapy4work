# -*- coding: utf-8 -*-

import pymysql
import asyncio
import aiomysql
import os
import re
from scrapy.exceptions import DropItem


class FilterBrandPipeline:
    """过滤违禁品"""

    def __init__(self, disallow_brand):
        self.disallow_brand = disallow_brand
        self.disallow_brand_list = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DISALLOW_BRAND'))

    def open_spider(self, spider):
        with open(self.disallow_brand, 'r') as f:
            self.disallow_brand_list = [line.strip() for line in f]

    def process_item(self, item, spider):
        for disallow_brand in self.disallow_brand_list:
            if re.match(item.get('brand'), disallow_brand, flags=re.I):
                raise DropItem('disallow brand!')
        return item


class MysqlPipeline:
    """常规mysql，阻塞式"""

    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('MYSQL_HOST'),
            crawler.settings.get('MYSQL_USER'),
            crawler.settings.get('MYSQL_PASSWORD'),
            crawler.settings.get('MYSQL_DATABASE'),
            crawler.settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(**self._get_db_info())

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        with self.conn.cursor() as cursor:
            cursor.execute(self._get_sql(item), tuple(item.values()))
            self.conn.commit()
        return item

    def _get_db_info(self):
        """返回数据库连接信息"""
        return {
            'host': self.host,
            'port': 3306,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': 'utf8'
        }

    def _get_sql(self, data):
        """生成sql语句"""
        keys = ','.join(data.keys())
        values_placeholder = ','.join(('%s',) * len(data))

        return f'insert into {self.table}({keys}) values({values_placeholder})'


class AioMysqlPipeline(MysqlPipeline):
    """异步mysql，非阻塞"""

    def __init__(self, *args):
        super(AioMysqlPipeline, self).__init__(*args)
        if os.name == 'posix':
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    def open_spider(self, spider):
        self.loop.run_until_complete(self.open_conn())

    def close_spider(self, spider):
        super(AioMysqlPipeline, self).close_spider(spider)
        self.loop.close()

    def process_item(self, item, spider):
        self.loop.run_until_complete(self.save(item))
        return item

    def _get_db_info(self):
        """
        修复aiomysql.connect()的参数
        `数据库名`在mysql.connect()中为`database`，而在aiomysql中为`db`
        另外，aiomysql.connect()需要额外的`loop`参数
        """
        db_info = super(AioMysqlPipeline, self)._get_db_info()
        db_info.update({'db': db_info['database'], 'loop': self.loop})
        db_info.pop('database')
        return db_info

    async def open_conn(self):
        self.conn = await aiomysql.connect(**self._get_db_info())

    async def save(self, item):
        async with self.conn.cursor() as cursor:
            await cursor.execute(self._get_sql(item), tuple(item.values()))
            await self.conn.commit()
