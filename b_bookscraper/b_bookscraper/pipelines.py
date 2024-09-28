# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class BBookscraperPipeline:
    def process_item(self, item, spider):
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("books.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT,
                price TEXT,
                availability TEXT,
                url TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO books (title, price, availability, url) VALUES (?, ?, ?, ?)
        ''', (item['title'], item['price'], item['availability'], item['url']))
        self.connection.commit()
        # pass the item to the next pipeline (if any)
        return item
