import pytest
import sys

sys.path.insert(0, '/home/joseph/hacker-reddit/backend/scraper/pyscraper/webscraper')

import pyscraper

@pytest.mark.forked
def test_redditscrape():
    scraper = pyscraper.PyScraper()._get_scraper("https://www.reddit.com/r/GameDeals/")
    data = scraper.get()
    assert len([x for x in data]) > 0

@pytest.mark.forked
def test_twitterspider():
    scraper = pyscraper.PyScraper()._get_scraper("https://twitter.com/Tracker_Deals/")
    data = scraper.get()
    assert len([x for x in data]) > 0

@pytest.mark.forked
def test_htmlspider():
    scraper = pyscraper.PyScraper()._get_scraper("https://www.amazon.ca/gp/goldbox")
    data = scraper.get()
    assert len([x for x in data]) > 0

