# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

class LoldocumentPipeline(object):
    def process_item(self, item, spider):
        hero_detail_path = os.getcwd() + "\loldocument\hero_detail.txt"
        with open(hero_detail_path, 'a') as txt:
            str = json.dumps(dict(item), ensure_ascii=False)
            txt.write(str)

