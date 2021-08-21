# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import django
from itemadapter import ItemAdapter
from pipe2db import pipe

from .items import EcommerceCategoryItem, EcommerceProductItem

django.setup()



class WithscrapyPipeline:
    def process_item(self, item, spider):
        # item routing...
        if isinstance(item, EcommerceProductItem):
            return self.process_product_item(item)
        return item



    @pipe({
        'model': 'ecommerce.Product',
        'unique_key': 'product_id',
        'exclude_fields': ['_imgsrc'],
        'rename_fields': {
            'image_data': 'image'
        },
        'contentfile_fields': {
            'image_data': {
                'source_url_field': '_imgsrc'
            }
        },
        'foreignkey_fields': {
            'category': {
                'model': 'ecommerce.Category',
                'unique_key': ['category', 'subcategory']
            }
        }
    })
    def process_product_item(self, item):
        return item