from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.loader import ItemLoader
from re import match
import string

class TwitterItemLoader(ItemLoader):
    
    def filter(x):
        return None if ((x in 'https://http://' ) or (len(' '.join(y.strip() for y in x.replace("\\r\\n", '').split())) == 0)) else ' '.join(x.split())
    
    default_input_processor = TakeFirst()
    title_in = MapCompose(filter, str.strip)
    title_out = Identity()
    url_in = MapCompose(lambda x: 'https://twitter.com' + x)
    url_out = Identity()

class HTMLGridItemLoader(ItemLoader):

    def filter(x):
        # filter out unneccesary characters , mostly from craiglist
        return None if ((x in ['•', '·', 'hide', 'View more'] ) or ('h ago' in x) or ('mins ago' in x) or ('min ago' in x) or ('ends in' in x) or (len(x.strip()) == 0)) else x

    def urljoin_w_context(x, loader_context):
        url = loader_context.get('site_url')
        return (url + x) if not (x.startswith('https://') or (x.startswith('http://'))) else x

    default_input_processor = TakeFirst()
    title_in = MapCompose(filter)
    title_out = Identity()
    url_in = MapCompose(urljoin_w_context)
    url_out = Identity()