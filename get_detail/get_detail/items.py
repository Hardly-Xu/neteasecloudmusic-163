# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class get_detail(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    resolution = scrapy.Field()
    camera = scrapy.Field()
    cpu = scrapy.Field()
    brand = scrapy.Field()
    product_id = scrapy.Field()
    more_info = scrapy.Field()
    spider = scrapy.Field()
    #有关评价
    CommentCount = scrapy.Field()
    GoodCount = scrapy.Field()
    DefaultGoodCount = scrapy.Field()
    GoodRate = scrapy.Field()
    PoorCount = scrapy.Field()
    PoorRate = scrapy.Field()
    AfterCount = scrapy.Field()