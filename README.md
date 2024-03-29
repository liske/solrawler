# solrawler - Simple Python SOLR Web Crawler

*solrawler* is a simple python based web crawler for SOLR. It uses the following python packages:

- [Scrapy](https://scrapy.org/) for web crawling
- [pysolr](https://github.com/django-haystack/pysolr) for SOLR API access
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML text extraction
- [pypdf2](https://mstamy2.github.io/PyPDF2/) for PDF text extraction

It is designed to be run inside docker. There are two environment variables to configure *solrawler*:

- `SOLRAWLER_SOLR` - the SOLR API url including the core (default: `http://solr:8983/solr/solrawler`)
- `SOLRAWLER_WAIT` - wait time in seconds between crawling runs, used by entrypoint (default: `8400`s)

You need to supply spider classes implementation to make the web crawler work:

- create a empty directory with a emptry `__init__.py` file
- add you spider defintion:
```
import scrapy
from solrawler.common import CommonSpider


class FiaskoSpider(CommonSpider):
    name = 'fiasko'
    allowed_domains = ['fiasko.io']
    start_urls = ['https://fiasko.io/']
```

Take a look at the supplied [docker-compose.yml](docker-compose.yml) file howto run *solrawler*.
