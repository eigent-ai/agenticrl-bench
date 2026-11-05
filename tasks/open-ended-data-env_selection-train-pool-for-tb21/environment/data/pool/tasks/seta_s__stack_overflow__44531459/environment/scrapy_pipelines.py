import csv


class CsvWriterPipeline:
    def open_spider(self, spider):
        self.file = open('items.csv', 'wb')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['name', 'price', 'category', 'source_page'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([
            item['name'],
            item['price'],
            item['category'],
            item['source_page'],
        ])
        return item
