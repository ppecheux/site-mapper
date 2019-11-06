import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class HeaderSpider(scrapy.Spider):
    name = 'headerbot'
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        # Extracting the content using css selectors
        title = response.xpath('//title/text()').get()
        body_length = len(response.xpath('body').get())
        recipes = LinkExtractor().extract_links(response)
        links = [recipe.url.split('#')[0] for recipe in recipes]

        # Give the extracted content row wise
        scraped_info = {
            'title': title,
            'body_length': body_length,
            'url': response.request.url,
            'links': links
            # add anchors to show the structure of the page?
        }

        # yield or give the scraped info to scrapy
        yield scraped_info

        for link in links:
            yield response.follow(link, self.parse)


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'pages.json'
    })
    HeaderSpider.allowed_domains = ['www.carisiolas.com']
    HeaderSpider.start_urls = ['https://www.carisiolas.com/']
    process.crawl(HeaderSpider)
    process.start()
