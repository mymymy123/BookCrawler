# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from BookCrawler.items import BookItem,CommentItem
import pymongo
import scrapy_redis

class MongoDBItemPipeline(object):
    @classmethod
    def from_crawler(cls,crawler):
        cls.connection_string=crawler.settings.get('MONGODB_CONNECTION_STRING')
        cls.database=crawler.settings.get('MONGODB_DATABASE')
        cls.collectoins=crawler.settings.get('MONGODB_COLLECTIONS')
        return cls()

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.connection_string)
        self.db=self.client[self.database]

    def process_item(self,item,spider):
        if isinstance(item,BookItem):
            book_collecton=self.db[self.collectoins['books']]
            book_collecton.update_one({
                'id':item['id']
            },{
                '$set':dict(item)
            },upsert=True)

        if isinstance(item,CommentItem):
            comment_collectoin=self.db[self.collectoins['comments']]
            comment_collectoin.update_one({
                'id':item['id']
            },{
                '$set':dict(item)
            },upsert=True)
        return item

    def close_spider(self,spider):
        self.client.close()