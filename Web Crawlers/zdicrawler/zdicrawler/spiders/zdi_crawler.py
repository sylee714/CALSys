import scrapy


class ZdiCrawlerSpider(scrapy.Spider):
    name = 'zdi_crawler'
    allowed_domains = ['https://www.zerodayinitiative.com/']
    start_urls = ['https://www.zerodayinitiative.com/advisories/published/2020/']

    def parse(self, response):
        print("processing:" + response.url)
        print(response.text)
