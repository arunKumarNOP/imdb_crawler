# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    movie_id = scrapy.Field()
    recommen_id = scrapy.Field()

    def __str__(self):
        return ""

class MovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    movie_name = scrapy.Field()

    def __str__(self):
        return ""