from django.contrib import admin

# Register your models here.
from .models import ScrapyProcess
from .process import start_scrapy_ecommerce




@admin.register(ScrapyProcess)
class ScrapyProcessAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = 'process_name',
    actions = ['start_process']

    def start_process(self, request, queryset):
        start_scrapy_ecommerce()
        