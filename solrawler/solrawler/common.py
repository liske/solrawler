# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from solrawler.items import SolrawlerItem
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import PyPDF2

from collections import OrderedDict
import io
import re


class CommonSpider(scrapy.Spider):
    seen = set()
    bs4_blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        'title',
    ]

    def parse(self, response):
        if response.url in self.seen:
            self.log('already seen  %s' % response.url)
        else:
            self.log('parsing  %s' % response.url)
            self.seen.add(response.url)

            # create item with generic values
            item = SolrawlerItem()
            item['solr'] = {
                'title': response.url,
                'id': response.url,
            }

            # copy some http headers
            for header, field in OrderedDict([
                ('Content-Type', 'content-type'),
                ('Last-Modified', 'date'),
                ('Date', 'date'),
            ]).items():
                if header in response.headers:
                    if not field in item['solr']:
                        item['solr'][field] = response.headers[header].decode(
                            'ascii')

            # handle text/* MIME types
            if response.__class__.__name__ in ['TextResponse', 'HtmlResponse']:
                # handle html responses
                if response.__class__.__name__ == 'HtmlResponse':
                    # use BeautifulSoup for ease parsing
                    soup = BeautifulSoup(response.text, 'html5lib')

                    # get html title
                    if soup.title and soup.title.string:
                        item['solr']['title'] = soup.title.string

                    # extract body text
                    text = soup.find_all(text=True)

                    item['solr']['text'] = ''.join(
                        list(filter(lambda t: t.parent.name not in self.bs4_blacklist, text)))

                    # follow links
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href:
                            url = urljoin(response.url, href)
                            if not url in self.seen and not re.search(r'.(zip|jar|iso|jpg|jpeg|png|ico)$', url):
                                # self.log("yielding request " + url)
                                yield Request(url, callback=self.parse)

                # handle everything else as plain text response
                else:
                    item['solr']['text'] = response.text

                # strip and remove duplicate spaces
                item['solr']['text'] = re.sub(
                    '\n\s+', '\n', re.sub('[ \t]+', ' ', item['solr']['text'])).strip()

                yield item

            # handle application/pdf MIME type
            elif item['solr'].get('content-type', '') == 'application/pdf':
                with io.BytesIO(response.body) as st:
                    pdf = PyPDF2.PdfFileReader(
                        st, strict=False, overwriteWarnings=False)

                    # get title from documentInfo
                    titles = []
                    di = pdf.getDocumentInfo()
                    for field in ['/Title', '/Subject']:
                        if field in di and di[field]:
                            titles.append(di[field])
                    if titles:
                        item['solr']['title'] = ', '.join(titles)

                    # extract text content from pages
                    idx = 0
                    item['solr']['text'] = ''

                    while idx < pdf.numPages:
                        page = pdf.getPage(idx)
                        idx += 1
                        item['solr']['text'] += ' ' + page.extractText()

                    # strip and remove duplicate spaces
                    item['solr']['text'] = re.sub(
                        '\n\s+', '\n', re.sub('[ \t]+', ' ', item['solr']['text'])).strip()

                    yield item

            # unhandled MIME type
            else:
                self.log(' unhandled MIME type {}'.format(
                    item['solr'].get('content-type', 'None')))
