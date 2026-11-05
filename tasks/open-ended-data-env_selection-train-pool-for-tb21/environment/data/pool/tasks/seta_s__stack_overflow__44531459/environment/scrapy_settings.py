BOT_NAME = "scrapy_project"

SPIDER_MODULES = ["scrapy_project.spiders"]
NEWSPIDER_MODULE = "scrapy_project.spiders"

ROBOTSTXT_OBEY = False
LOG_LEVEL = "INFO"

# ITEM_PIPELINES = {
#     "scrapy_project.pipelines.CsvWriterPipeline": 300,
# }

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
