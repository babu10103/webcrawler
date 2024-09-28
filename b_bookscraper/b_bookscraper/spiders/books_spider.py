import scrapy
from b_bookscraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Extracting book details
        for book in response.css('article.product_pod'):
            item = BookItem()  # Create an instance of the BookItem

            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('div.product_price p.price_color::text').get()
            item['availability'] = book.css('p.instock.availability::text').re_first('\S+')
            item['url'] = response.url

            # Yield the item to the pipeline for further processing
            yield item

        # Handling pagination and moving to the next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Moving to the next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)

    def errback(self, failure):
        self.logger.error(f"Request failed with error: {failure}")
