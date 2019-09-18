# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class LoldocumentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    DATAname = scrapy.Field()
    DATAtitle = scrapy.Field()
    DATAtags = scrapy.Field()
    DATAinfo = scrapy.Field()
