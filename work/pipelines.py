# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import aiomysql


class MysqlPipeline:

    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.db = None
        self.cursor = None

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
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=3306, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values_placeholder = ','.join(('%s',) * len(data))

        sql = f'insert into {self.table}({keys}) values({values_placeholder})'

        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()

        return item


class AioMysqlPipeline:
    pass
