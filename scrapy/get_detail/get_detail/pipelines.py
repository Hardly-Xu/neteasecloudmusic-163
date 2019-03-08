# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
r= redis.Redis(host='127.0.0.1',password='123321',port=6379,db=0)

class ScrapyRedisJdPipeline(object):
    def process_item(self, item, spider):
        item["spider"] = '数据来自:'+spider.name
        return item 
