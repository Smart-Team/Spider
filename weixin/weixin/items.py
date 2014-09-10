# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field




class WeixinSubjectItem(Item):
    title = Field()
    link = Field()
    content = Field()
    date = Field()
    author = Field()
    image = Field()
