# -*- coding: utf-8 -*-


import pymysql
import asyncio
import uvloop
import aiomysql


class MysqlPipeline:
    """ 常规mysql，阻塞式"""

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
        self.conn = pymysql.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values_placeholder = ','.join(('%s',) * len(data))

        sql = f'insert into {self.table}({keys}) values({values_placeholder})'

        with self.conn.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))

        self.conn.commit()
        return item


class AioMysqlPipeline(MysqlPipeline):
    """ 异步mysql，非阻塞"""

    def __init__(self, host, user, password, database, table):
        super(AioMysqlPipeline, self).__init__(host, user, password, database, table)
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    @classmethod
    def from_crawler(cls, crawler):
        return super(AioMysqlPipeline, cls).from_crawler(crawler)

    def open_spider(self, spider):
        self.loop.run_until_complete(self.open_conn())

    def close_spider(self, spider):
        self.conn.close()
        self.loop.close()

    def process_item(self, item, spider):
        self.loop.run_until_complete(self.save(item))
        return item

    async def open_conn(self):
        self.conn = await aiomysql.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            db=self.database,
            charset='utf8',
            loop=self.loop
        )

    async def save(self, item):
        data = dict(item)
        keys = ','.join(data.keys())
        values_placeholder = ','.join(('%s',) * len(data))

        sql = f'insert into {self.table}({keys}) values({values_placeholder})'

        async with self.conn.cursor() as cursor:
            await cursor.execute(sql, tuple(data.values()))
            await self.conn.commit()
