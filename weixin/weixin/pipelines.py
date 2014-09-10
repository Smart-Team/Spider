# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals


import json
import codecs


class JsonWithEncodingPipeline(object):

    def __init__(self):
        #self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        _item = dict(item)
        line = json.dumps(_item, ensure_ascii=False) + "\n"
        #line = _item['title'] + "\n"
        
#        file_name = _item['p_class'] + '-' +_item['s_class']
#        file_name = file_name.encode('utf-8')
        file_name = "data.utf8";
        print file_name 
        
        self.write(line, file_name)
        
        #print line
        
        #self.file.write(line)
        return item

    def write(self, line, name):
        self.file = codecs.open("data/"+name+".json", 'a', encoding='utf-8')
        self.file.writelines(line)
        

    def spider_closed(self, spider):
        self.file.close()
