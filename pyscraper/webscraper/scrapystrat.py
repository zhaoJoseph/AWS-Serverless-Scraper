from strategy import ScrapeStrategy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals

from webscraper import settings as my_settings
import os, sys

class ScrapyStrat(ScrapeStrategy):

    def __init__(self, spider, url):
        self.spider = spider
        self.url = url
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', my_settings.__name__)
        self.process = CrawlerProcess(get_project_settings())

    def get(self):
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        self.process.crawl(
            self.spider.__class__, 
            url=self.url, 
            )
        self.process.start()
        return results

class HtmlStrat(ScrapeStrategy):

    def __init__(self, spider, url, className):
        self.spider = spider
        self.url = url
        self.className = className
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', my_settings.__name__)
        self.process = CrawlerProcess(get_project_settings())

    def get(self):
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        self.process.crawl(
            self.spider.__class__, 
            url=self.url, 
            className=self.className,
            )
        self.process.start()
        return results