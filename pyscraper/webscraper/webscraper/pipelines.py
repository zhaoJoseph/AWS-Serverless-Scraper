from scrapy.exceptions import DropItem, NotConfigured
from re import match

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TitlePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if (adapter.get("title") and (len(adapter["title"]) > 0)):

            title = ' '.join(list(dict.fromkeys(adapter['title']))).strip()

            adapter['title'] =  title

            return item
        else:
            raise DropItem(f"Missing Title in {item}")

class UrlPipeline: 
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        if (not adapter.get('url')) or (len(adapter['url']) < 1):
            raise DropItem(f"Missing Url in {item}")
        else:
            adapter = ItemAdapter(item)

            url = adapter['url'][0]

            adapter['url'] =  url

            return item

class DuplicatesPipeline:
    
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['title'] in self.titles_seen:
            raise DropItem(f"Duplicate title found: {item!r}")
        else:
            self.titles_seen.add(adapter['title'])
            return item


class PricesPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('PRICESPIPELINE'):
            # if this isn't specified in settings, the pipeline will be completely disabled
            raise NotConfigured
        return cls()


    def process_price(self, titles):
        price_pattern = r"^(?:CA?\$|C\$|\$)"
        number_pattern = r"^\d+$"
        prices_copy = titles
        processed_titles = []
        while len(prices_copy) > 0:
            item = prices_copy.pop(0)
            if len(prices_copy) == 0:
                processed_titles.append(item)
                break
            if match(price_pattern, item) and match(price_pattern, prices_copy[0]):
                change_price = prices_copy.pop(0)

                price_change = "new: " + item + ", old:" + change_price if item < change_price else  "new: " + change_price + ", old:" + item
                processed_titles.append(price_change)
            elif match(price_pattern, item) and match(number_pattern, prices_copy[0]):
                end_price = prices_copy.pop(0)
                price = item + "." + end_price
                processed_titles.append(price)
            else:
                processed_titles.append(item)
        return processed_titles

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if (adapter.get("title") and (len(adapter["title"]) > 0)):

            title_list = self.process_price(adapter["title"])

            adapter['title'] =  title_list

            return item
        else:
            raise DropItem(f"Missing Title in {item}")

    