from django.db import models
from django.db.models import Model



class ScrapyProcess(models.Model):
    process_name = models.CharField(
        'Process Name', max_length=50, choices=[('withscrapy.process.start_scrapy_ecommerce', 'start_scrapy_ecommerce')]
    )
    
    def __str__(self) -> str:
        return self.process_name        

