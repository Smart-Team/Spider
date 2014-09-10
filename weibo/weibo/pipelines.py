# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo.connection import MongoClient
from scrapy import log
import datetime

class WeiboPipeline(object):
    def process_item(self, item, spider):
        print item;
        return item


class SingleMongodbPipeline(object):
    """
        save the data to mongodb.
    """

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "weibo_fs"

    def __init__(self):
        try:
            client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT) 
            self.db = client[self.MONGODB_DB]
        except Exception as e:
            print "ERROR(SingleMongodbPipeline): %s"%(str(e),)


    def process_item(self, item, spider):
        weibo_detail = {
            'id':item.get('id',''),
            'desc':item.get('desc',''),
            'c_time':item.get('c_time',''),
            'source':item.get('source',''),
            'update_time':datetime.datetime.utcnow(),
        }
        
        result = self.db['weibo'].insert(weibo_detail)

        log.msg("Item %s wrote to MongoDB database %s/book_detail" %
                    (result, self.MONGODB_DB),
                    level=log.DEBUG, spider=spider)
        return item