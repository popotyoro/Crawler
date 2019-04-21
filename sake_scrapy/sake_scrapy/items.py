# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SakeScrapyItem(scrapy.Item):
    prefecture = scrapy.Field()
    kuramoto = scrapy.Field()
    sake_name = scrapy.Field()

