from django.contrib import admin

# Register your models here.
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = 'category', 'subcategory'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = 'category', 'product_id', 'product_name', 'price', 'href',
