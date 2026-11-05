import scrapy
from scrapy_project.items import ProductItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = ["http://localhost:8888/"]

    def parse(self, response):
        links = response.css("a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        category_name = response.css("h1::text").get("").strip().lower()
        for product in response.css("div.product"):
            item = ProductItem()
            item["name"] = product.css("span.name::text").get("").strip()
            item["price"] = product.css("span.price::text").get("").strip()
            item["category"] = category_name
            item["source_page"] = response.url
            yield item
