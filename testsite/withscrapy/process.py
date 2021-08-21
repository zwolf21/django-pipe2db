from billiard.context import Process
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess


from .spiders.ecommerceio import EcommerceioSpider


def crawling():
    settings = Settings()
    settings.setmodule('withscrapy.settings')
    crawler = CrawlerProcess(settings=settings)
    crawler.crawl(EcommerceioSpider)
    crawler.start()


def start_scrapy_ecommerce():
    proc = Process(target=crawling)
    proc.start()
    proc.join()

