# -*- coding: utf-8 -*-
import scrapy
from solrawler.common import CommonSpider


class FiaskoSpider(CommonSpider):
    name = 'fiasko'
    allowed_domains = ['fiasko.io']
    start_urls = ['https://fiasko.io/']