# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class SaveItemPipeline(object):
    def __init__(self):
        self.filename = "ziroomHangzhou.jl"

    def open_spider(self, spider):
        # 使用 codecs 编码问题较好处理，http://www.cnblogs.com/buptldf/p/4805879.html
        self.file = codecs.open(self.filename, 'a', 'utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # ensure_ascii 设置为 false，输出为中文
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item
