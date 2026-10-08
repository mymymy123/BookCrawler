# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    publisher = scrapy.Field()
    page_number = scrapy.Field()
    isbn = scrapy.Field()
    published_at = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    authors = scrapy.Field()
    translators = scrapy.Field()
    score = scrapy.Field()
    catalog = scrapy.Field()
    cover = scrapy.Field()
    introduction = scrapy.Field()
    

class CommentItem(scrapy.Item):
    id=scrapy.Field()
    content=scrapy.Field()
    book_id=scrapy.Field()


