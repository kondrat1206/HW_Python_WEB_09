import scrapy
import json
from quotes_scraper.quotes_scraper.items import QuoteItem, AuthorItem


class QuoteSpider(scrapy.Spider):

    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']
    items = []

    def parse(self, response):
        # Парсинг цитат
        for quote in response.css('div.quote'):
            quote_item = {
                'tags': quote.css('div.tags a.tag::text').getall(),
                'author': quote.css('span > small.author::text').get(),
                'quote': quote.css('span.text::text').get()
            }
            self.items.append(quote_item)
            yield quote_item

        # Переход на следующую страницу, если она существует
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def close(self, reason):
        # Запись цитат в JSON
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.items, ensure_ascii=False, indent=2))


class AuthorSpider(scrapy.Spider):

    name = 'authors'
    start_urls = ['http://quotes.toscrape.com']
    items = []


    def parse(self, response):

        # Выбор цитат
        for quote in response.css('div.quote'):
            # Переход на URL автора
            author_url = quote.css('span > small.author + a::attr(href)').get()
            if author_url:
                yield response.follow(author_url, callback=self.parse_author)

        # Переход на следующую страницу, если она существует
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_author(self, response):

        # Парсинг информации об авторе
        author_item = {
            'fullname': response.css('h3.author-title::text').get(),
            'born_date': response.css('span.author-born-date::text').get(),
            'born_location': response.css('span.author-born-location::text').get(),
            'description': response.css('div.author-description::text').get()
        }
        self.items.append(author_item)
        yield author_item


    def close(self, reason):
        # Запись цитат в JSON
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.items, ensure_ascii=False, indent=2))

