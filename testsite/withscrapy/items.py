# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommerceCategoryItem(scrapy.Item):
    category = scrapy.Field()
    subcategory = scrapy.Field()


class EcommerceProductItem(scrapy.Item):
    category = scrapy.Field()
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    href = scrapy.Field()
    image_data = scrapy.Field()
    _imgsrc = scrapy.Field()