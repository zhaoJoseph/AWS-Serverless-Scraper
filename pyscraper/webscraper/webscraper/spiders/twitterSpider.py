import scrapy
from scrapy.selector import Selector
from webscraper.items import HTMLItem
from webscraper.itemloaders import TwitterItemLoader

class TwitterSpider(scrapy.Spider):
    name='twitter'
 
    def start_requests(self):
        url=f'https://twitter.com/{self.url}'
        yield scrapy.Request(
            url=url, 
            callback=self.parse, 
            meta= dict(
                            playwright = True,
                            playwright_include_page = True,
                        ),
            errback=self.close_page,
        )

    def has_social_context(self, element):
        social_context = element.css('[data-testid="socialContext"]')
        if social_context:
            return True

        descendant_social_context = element.css('* [data-testid="socialContext"]')
        if descendant_social_context:
            return True

        return False

    async def parse(self, response):
        
        page = response.meta["playwright_page"]

        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await page.wait_for_timeout(6000)
        html = await page.content()
        await page.close()

        res = Selector(text=html)
        href_select = 'a.css-4rbku5.css-18t94o4.css-901oao.r-14j79pv.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0::attr(href)'
        tweets = res.css('[data-testid="tweet"]').getall()
        
        for elem in tweets:
            select = Selector(text=elem)
            if not self.has_social_context(select):
                twitterProduct = TwitterItemLoader(item=HTMLItem(), selector=select)
                twitterProduct.add_css("title", 'div[data-testid="tweetText"] *::text')
                twitterProduct.add_css("url", href_select)
                yield twitterProduct.load_item()


    async def close_page(self, error):
        page = error.request.meta['playwright_page']
        await page.close()

