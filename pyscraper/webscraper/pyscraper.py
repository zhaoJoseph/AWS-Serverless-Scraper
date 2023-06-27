from urllib.parse import urlparse
from scrapystrat import ScrapyStrat, HtmlStrat
from apistrat import ApiStrat
from webscraper.spiders.twitterSpider import TwitterSpider
from apiscraper.redditscrape import RedditApi
from webscraper.spiders.htmlgrid import HTMLGridSpider
import sys
import os

classNames = {
    "https://www.amazon.ca/gp/goldbox" : "DealGridItem-module__dealItemDisplayGrid_e7RQVFWSOrwXBX4i24Tqg",
    "https://store.steampowered.com/specials/?flavor=contenthub_newandtrending&offset=12" : "salepreviewwidgets_SaleItemBrowserRow_y9MSd",
    "https://store.epicgames.com/en-US/free-games" : "css-aere9z",
    "https://sale.alibaba.com/p/weekly_deals/new.html?wx_navbar_transparent=true&path=/p/weekly_deals/new.html&ncms_spm=a27aq.weekly_deals&prefetchKey=met" : "hugo3-pc-grid-item",
    "https://www.wish.com/~/trending/": "ProductGrid__FeedTileWidthWrapper-sc-122ygxd-2",
    "https://www.gog.com/en/games/discounted" : "product-tile",
    "https://www.humblebundle.com/store/promo/on-sale-now" : "entity-block-container",
    "https://ottawa.craigslist.org/search/sss" : "cl-search-result",
    "https://toronto.craigslist.org/search/sss" : "cl-search-result",
    "https://newyork.craigslist.org/search/sss" : "cl-search-result",
    "https://chicago.craigslist.org/search/sss" : "cl-search-result",
    "https://montreal.craigslist.org/search/sss" : "result-row",
    "https://vancouver.craigslist.org/search/sss" : "cl-search-result",
    "https://calgary.craigslist.org/search/sss" : "cl-search-result",
    "https://boston.craigslist.org/search/sss" : "cl-search-result",
    "https://seattle.craigslist.org/search/sss" : "cl-search-result",
    "https://sfbay.craigslist.org/search/sss" : "cl-search-result",
    "https://www.ebay.ca/deals" : "col",
    "https://www.retailmenot.com/ca/" : "offerItem",
    "https://www.dontpayfull.com/at/play.google.com" : "obox",
    "https://www.f6s.com/deals?category=cloud-services&sort=newest&sort_dir=desc": "result-item",
    "https://store.epicgames.com/en-US/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&category=Game&count=40&start=0" :  "css-lrwy1y",
    "https://www.coupons.com/top-offers" : "_1abe9s97"  
}


class PyScraper:

    def _get_scraper(self, url):
        base_url = urlparse(url).netloc
        if base_url == 'twitter.com':
            twitterHandler = url.split('/')[-2]
            return ScrapyStrat(TwitterSpider(), twitterHandler)
        elif base_url == 'www.reddit.com':
            subreddit = url.split('/')[-2]
            return ApiStrat(RedditApi(subreddit=subreddit))
        else:
            return HtmlStrat(HTMLGridSpider(), url, classNames[url])

    def execute(self, url):
        scraper = self._get_scraper(url)
        data = scraper.get()
        print(data)

if __name__ == '__main__':

    if ('AWS_BATCH_JOB_ARRAY_INDEX' in os.environ ) and int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX']) and ( 'URL_ARRAY' in os.environ):
        urlArray = os.environ['URL_ARRAY']
        url = urlArray[int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])]
    elif len(sys.argv) < 2 : 
        raise Exception("Error: url not supplied")
    else:
        url = sys.argv[1]
    pyscrape = PyScraper()
    pyscrape.execute(url)
