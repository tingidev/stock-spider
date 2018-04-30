# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    date = scrapy.Field()
    date_str = scrapy.Field()
    acronym = scrapy.Field()
    name = scrapy.Field()
    pe_val = scrapy.Field()
    volume = scrapy.Field()
    price = scrapy.Field()