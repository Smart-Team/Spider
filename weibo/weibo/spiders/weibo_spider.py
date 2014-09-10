#! /usr/bin/env python
# encoding:utf-8

import scrapy
import json

from scrapy.http.request import Request 
from weibo.items import WeiboItem

class WeiboOrg(scrapy.Spider):
    name = "weibo_org"
    allowed_domains = ["weibo.cn"]
    
    gsid = {'gsid_CTandWM': '4uPha9c61wGOjPHMDFTGxmb0E1g'};
    
    level = 0;
    
    start_urls = [
        "http://m.weibo.cn/index/feed?format=cards&uicode=20000174&rl=1&next_cursor=0",
    ]
    
    def start_requests(self):  
        for url in self.start_urls:          
            yield Request(url, cookies=self.gsid) 


    def parse(self, response):
        data = json.loads(response.body);
 
        for ob in data.get('cards')[0].get('card_group'):
            item = WeiboItem();
            mblog = ob.get('mblog');
            
            item['id'] = mblog.get('id');
            item['desc'] = mblog.get('text');
            item['c_time'] = mblog.get('created_at');
            item['source'] = mblog.get('source');
            
            yield item;
            
        #递归抓取数据
        next_url = response.url.split("next_cursor")[0] + "next_cursor=" + str(data.get('next_cursor',''));
        
        if(++self.level < 50):
            yield Request(next_url, cookies=self.gsid, callback=self.parse)
        



class WeiboPub(scrapy.Spider):
    name = "weibo_pub"
    allowed_domains = ["weibo.cn"]
    
    gsid = {'gsid_CTandWM': '4uPha9c61wGOjPHMDFTGxmb0E1g'};
    
    level = 0;
    
    start_urls = [
        "http://m.weibo.cn/page/json?containerid=1005052028810631_-_WEIBO_SECOND_PROFILE_WEIBO&uicode=10000012&fid=1005052028810631_-_WEIBO_SECOND_PROFILE_WEIBO&ext=sourceType&rl=1&page=%d" % d for d in range(1, 100)
    ]
    
    def start_requests(self):  
        for url in self.start_urls:          
            yield Request(url, cookies=self.gsid) 


    def parse(self, response):
        data = json.loads(response.body);
 
        list = data.get('cards')[0].get('card_group', -1);
        if(list == -1):
            list = data.get('cards');
        
        
        for ob in list:
            item = WeiboItem();
            mblog = ob.get('mblog');
            
            item['id'] = mblog.get('id');
            item['desc'] = mblog.get('text');
            item['c_time'] = mblog.get('created_at');
            item['source'] = mblog.get('user').get('screen_name');
            
            yield item;
            
            
    