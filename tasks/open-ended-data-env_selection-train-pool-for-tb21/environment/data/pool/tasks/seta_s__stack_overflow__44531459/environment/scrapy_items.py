import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    source_page = scrapy.Field()
