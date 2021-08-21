import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pathlib import Path
from bs4 import BeautifulSoup


from ..items import EcommerceCategoryItem, EcommerceProductItem

class EcommerceioSpider(CrawlSpider):
    name = 'ecommerceio'
    # allowed_domains = ['webscraper.io']
    start_urls = ['https://webscraper.io/test-sites/e-commerce/allinone/']


    def start_requests(self):
        yield scrapy.Request('https://webscraper.io/test-sites/e-commerce/allinone/', callback=self.parse_category)


    def parse_category(self, response):

        for link in response.xpath(".//a[contains(@class, 'category-link')]//@href").getall():
            p = Path(response.url)
            item = EcommerceCategoryItem(
                category=p.stem
            )
            yield response.follow(
                link, callback=self.parse_subcategory, cb_kwargs={'category_item': item}
            )
    

    def parse_subcategory(self, response, category_item):
        for link in response.xpath(".//a[contains(@class, 'category-link')]//@href").getall():
            p = Path(response.url)
            category_item['subcategory'] = p.stem
            yield category_item
            yield response.follow(link, callback=self.parse_product_list, cb_kwargs={'category_item': category_item})

    
    def parse_product_list(self, response, category_item):
        def parse_thumnail_area(area):
            price = area.xpath(".//h4[contains(@class, 'price')]//text()").get()
            area_title = area.xpath(".//a[contains(@class, 'title')]")
            title = area_title.xpath(".//text()").get('')
            product_url = area_title.xpath("./@href").get()
            scrapy.Request
            return EcommerceProductItem(
                category=category_item, # inject foreign field item!
                product_id=Path(product_url).stem,
                product_name=title,
                price=price,
                href=area_title.xpath('.//@href').get(),
                _imgsrc=area.xpath(".//img//@src").get()
            )

        for item_area in response.xpath(".//div[contains(@class, 'thumbnail')]"):
            item = parse_thumnail_area(item_area)
            if imgsrc := item.get('_imgsrc'):
                yield response.follow(
                        imgsrc, callback=self.load_product_image_data, cb_kwargs={'product_item': item},
                        dont_filter=True,
                    )

            # yield item

    
    def load_product_image_data(self, response, product_item):
        product_item['image_data'] = response.body
        yield product_item
            










    