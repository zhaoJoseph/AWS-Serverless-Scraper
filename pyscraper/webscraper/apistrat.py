from strategy import ScrapeStrategy

class ApiStrat(ScrapeStrategy):

    def __init__(self, scraper):
        self.scraper = scraper

    def get(self):
        data = self.scraper.get()
        return [x for x in self.scraper.collect(data)]