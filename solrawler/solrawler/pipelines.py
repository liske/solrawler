# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pysolr
from urllib.parse import urlparse
import os
import socket


class SolrawlerPipeline(object):
    base_url = os.getenv('SOLRAWLER_SOLR', 'http://solr:8983/solr/solrawler')

    def wait_solr(self):
        p = urlparse(self.base_url)
        s = socket.socket()
        while True:
            try:
                s.connect((p.hostname, p.port or 80))
                s.close()
                return
            except:
                pass

    def open_spider(self, spider):
        self.wait_solr()
        self.solr = pysolr.Solr(self.base_url, timeout=10)

    def process_item(self, item, spider):
        self.solr.add([item['solr']])
        return item

    def close_spider(self, spider):
        self.solr.commit()
