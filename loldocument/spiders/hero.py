# -*- coding: utf-8 -*-
import scrapy
from loldocument.items import LoldocumentItem
import os
import urllib.request
import re
class HeroSpider(scrapy.Spider):
    name = 'hero'
    allowed_domains = ['lol.qq.com']
    start_urls = ['https://lol.qq.com/data/info-heros.shtml']
    def __init__(self):
        '''每次执行之前先删除之前的数据，保证数据全是最新的'''
        hero_detail_path =  os.getcwd() + "\loldocument\hero_detail.txt" # F:\loldocument\loldocument\hero_detail.txt
        print(os.path.exists(hero_detail_path))
        if os.path.exists(hero_detail_path):
            try:
                os.remove(hero_detail_path)
            except IOError:
                print('系统错误，无法删除文件-')
            else:
                print('移除文件：%s' % hero_detail_path)
        else:
            print("要删除的文件不存在！")
        hero_logo_dir = os.getcwd() + "\hero_logo"
        for root, dirs, files in os.walk(hero_logo_dir, topdown=False):
            for name in files:
                portion = os.path.splitext(name)
                if portion[1] == '.jpg':
                    os.remove(os.path.join(root, name))
                    print('删除logo---'+name+'成功')

    def parse(self, response):
        heros = response.xpath('//ul[@id="jSearchHeroDiv"]/li')
        # heros = [heros[0], heros[1]]
        for hero in heros:  # 遍历每个li
            imgu = 'http:' + hero.xpath("./a/img/@src").extract_first()
            title = hero.xpath("./a/@title").extract_first()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            req = urllib.request.Request(url=imgu, headers=headers)
            res = urllib.request.urlopen(req)
            path = r'F:\loldocument\hero_logo' # 保存英雄头像的路径
            if not os.path.exists(path):
                os.makedirs(path)
            file_name = os.path.join(r'F:\loldocument\hero_logo', title + '.jpg')
            with open(file_name, 'wb') as fp:
                fp.write(res.read())
            url = 'https://lol.qq.com/data/' + hero.xpath("./a/@href").extract_first()
            request = scrapy.Request(url=url, callback=self.parse_detail)
            request.meta['PhantomJS'] = True
            request.meta['title'] = title
            yield request

    def parse_detail(self, response):
        # 英雄详情
        item = LoldocumentItem()
        item['title'] = response.meta['title']
        item['DATAname'] = response.xpath('//h1[@id="DATAname"]/text()').extract_first()
        item['DATAtitle'] = response.xpath('//h2[@id="DATAtitle"]/text()').extract_first()
        item['DATAtags'] = response.xpath('//div[@id="DATAtags"]/span/text()').extract()
        infokeys = response.xpath('//dl[@id="DATAinfo"]/dt/text()').extract()
        infovalues = response.xpath('//dl[@id="DATAinfo"]/dd/i/@style').extract()
        item['DATAinfo'] = {} # 英雄属性
        for i,v in enumerate(infokeys):
            item['DATAinfo'][v] = re.sub(r'width:', "", infovalues[i])
        yield item