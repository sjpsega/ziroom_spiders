# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HouseItem(Item):
    # define the fields for your item here like:
    link = Field() #链接
    name = Field() #名称
    area = Field() #面积
    price = Field() #租金
    district = Field() #区
    nearestSubWayDist = Field() #最近地铁距离(m)