import re
import json


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.linkextractors import LinkExtractor

from weixin.items import *
import time


class WeixinSpider(CrawlSpider):
    name = "weixin_spider"
    #allowed_domains = ["douban.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?type=2&query=x",
        #"http://www.baidu.com/s?wd=x",
        
    ]
#    rules = [
#        #Rule(sle(allow=("http://www.baidu.com/link?")), callback='parse_2'),
#        #Rule(sle(allow=(r"http:\/\/mp\.weixin\.qq\.com\/s?__biz=.*")), callback='parse_2'),
#        #Rule(sle(allow=(r"http:\/\/weixin\.sogou\.com\/weixin?query=.*", )), follow=True),
#        
#        
#        Rule(LinkExtractor(allow=('http:\/\/mp\.weixin\.qq\.com\/s?__biz=.*', )), callback='parse_2'),
#        Rule(LinkExtractor(allow=('http:\/\/weixin\.sogou\.com\/weixin?query=.*', )), follow=True),
#        #Rule(sle(allow=(r'.*'), deny=(r'\/sogou\/')), callback='parse_2')
#    ]
    
    rules = [
#        Rule(LinkExtractor(allow=(".*", )), callback='parse_2'),
        Rule(LinkExtractor(allow=("http://weixin.sogou.com/.*", )), follow=True),
        Rule(LinkExtractor(allow=('http://mp.weixin.qq.com/s\?.*', )), callback='parse_2'),
    ]

    def parse_2(self, response):
        items = []
        
        time.sleep(0.5);
        
        print response;
        
        sel = Selector(response)
        content = sel.css('.rich_media .rich_media_inner');
        
        
        item = WeixinSubjectItem()
        item['title'] = content.xpath('//h2[@class="rich_media_title"]/text()').extract()[0].strip()
        item['date'] = content.xpath('//em[@id="post-date"]/text()').extract()[0].strip()
        item['author'] = content.xpath('//a[@id="post-user"]/text()').extract()[0].strip()
        item['link'] = response.url
        item['image'] = content.xpath('//div[@class="rich_media_thumb"]/text()').extract()
        item['content'] = content.xpath('//div[@class="rich_media_content"]').extract()
        items.append(item)

        print item['title'];
       
        # info('parsed ' + str(response))
        return items




