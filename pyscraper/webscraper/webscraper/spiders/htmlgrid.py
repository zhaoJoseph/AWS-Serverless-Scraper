import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
from webscraper.itemloaders import HTMLGridItemLoader
from webscraper.items import HTMLItem
from urllib.parse import urlparse

class HTMLGridSpider(scrapy.Spider):
    name='html'
    
    custom_settings={
            "PRICESPIPELINE": True,
            "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 240000,
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": None,
            "PLAYWRIGHT_CONTEXTS": {
                "default": {
                    "viewport": {
                        "width": 1920,
                        "height": 1080,
                    },
                }
            },
        }

    def base_url(self, site_url):
        parsed_uri = urlparse(site_url)
        return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    def start_requests(self):

        self.parsed_url = self.base_url(self.url)

        yield scrapy.Request(
            url=f'{self.url}', 
            callback=self.parse, 
            dont_filter=True,
            meta={
                "playwright": True,
                "playwright_include_page": True,
            },
            errback=self.close_page
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await page.wait_for_timeout(6000)
        html = await page.content()
        await page.close()

        res = Selector(text=html)
        elems = res.css(f'.{self.className}').getall()

        for elem in elems:
            select = Selector(text=elem)
            htmlLoader = HTMLGridItemLoader(item=HTMLItem(), selector=select)
            htmlLoader.context['site_url'] = self.parsed_url
            htmlLoader.add_xpath('title', './/text()[not(parent::script)]')
            htmlLoader.add_css('url', '*::attr(href)')
            yield htmlLoader.load_item()
 
    async def close_page(self, error):
        page = error.request.meta['playwright_page']
        print(page)
        await page.close()

    def close(self, spider, reason):
        print(reason)
        
