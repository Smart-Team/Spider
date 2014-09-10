#! /usr/bin/env python
# encoding:utf-8

import scrapy
import json

from scrapy.http.request import Request 
from weibo.items import WeiboItem

class WeiboSpider(scrapy.Spider):
    name = "weibo_spider"
    allowed_domains = ["weibo.cn"]
    start_urls = [
        "http://m.weibo.cn/index/feed?format=cards&next_cursor=3752836900829687&uicode=20000174&rl=1",
    ]
    
    def start_requests(self):  
        for url in self.start_urls:          
            yield Request(url, cookies={'gsid_CTandWM': '4uPha9c61wGOjPHMDFTGxmb0E1g'}) 


    def parse(self, response):
        data = json.loads(response.body);
        next_page = data.get('next_cursor','');
        
        return parseItem(data);
        

    def parseItem(self, data):
        items = []
        for ob in data.get('cards')[0].get('card_group'):
            item = WeiboItem();
            mblog = ob.get('mblog');
            
            item['id'] = mblog.get('id');
            item['desc'] = mblog.get('text');
            item['c_time'] = mblog.get('created_at');
            item['source'] = mblog.get('source');
            
            items.append(item);
            
        return items;

