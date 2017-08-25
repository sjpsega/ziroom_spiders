# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.shell import inspect_response
from ziroom.items import HouseItem


class ziroomSpider(scrapy.Spider):
    name = "ziroomHangzhou"

    def start_requests(self):
        urls = [
            # 'http://hz.ziroom.com/z/nl/z3.html',# 不限
            'http://hz.ziroom.com/z/nl/z3-d330102.html',
            'http://hz.ziroom.com/z/nl/z3-d330103.html',
            'http://hz.ziroom.com/z/nl/z3-d23009161.html',
            'http://hz.ziroom.com/z/nl/z3-d330110.html',
            'http://hz.ziroom.com/z/nl/z3-d330105.html',
            'http://hz.ziroom.com/z/nl/z3-d330104.html',
            'http://hz.ziroom.com/z/nl/z3-d330108.html',
            'http://hz.ziroom.com/z/nl/z3-d330109.html',
            'http://hz.ziroom.com/z/nl/z3-d330106.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.body:
            for li in response.xpath('//*[@id="houseList"]/li'):
                house_item = None
                name = li.xpath(
                    './/div[contains(@class,"txt")]/h3/a/text()').extract_first()
                link = li.xpath(
                    './/div[contains(@class,"txt")]/h3/a/@href').extract_first()
                district = li.xpath(
                    './/div[contains(@class,"txt")]/h4/a/text()').re_first(r'(\w+)')
                detail_node = li.xpath(
                    './/div[contains(@class,"txt")]/div[contains(@class,"detail")]')
                area = detail_node.xpath(
                    './/p[1]/span[1]/text()'). re_first(r'[\s\S]*?(\d+(?:\.\d+)?)[\s\S]*?')  # 整数、分数、约+整分数
                price = li.xpath(
                    './/div[contains(@class,"priceDetail")]/p[contains(@class,"price")]/text()').re_first(r'\s+(\d+.\d+)\s+')
                # self.log(u'name:{} - link:{} - district:{} - area:{} - price:{}'.format(name, link, district, area, price))
                house_item = HouseItem(
                    name=name, link=link, district=district, area=area, price=price)
                self.log(u'{}'.format(house_item))
                response.meta['house_item'] = house_item
                yield house_item
            # 访问下一页内容
            next = response.xpath(
                '//*[@id="page"]/a[contains(@class, "next")]')
            if next:
                next_href = next.xpath('.//@href').extract_first()
                yield response.follow(next_href, callback=self.parse)
        else:
            inspect_response(response, self)
            self.log('error!!!', logging.ERROR)
