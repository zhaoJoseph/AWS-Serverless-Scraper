import pytest
import sys
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, env['MODULE_PATH'])

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

