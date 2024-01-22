from scrapy.crawler import CrawlerProcess
from quotes_scraper.quotes_scraper.spiders import quotes_spider
from search_quotes import main


def processing():
    # Запуск процесса парсинга
    process = CrawlerProcess()
    process.crawl(quotes_spider.QuoteSpider, output_file="quotes.json")
    process.crawl(quotes_spider.AuthorSpider, output_file="authors.json")
    process.start()


if __name__ == "__main__":
    processing()
    main()