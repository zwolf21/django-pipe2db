from django.db import models


class Category(models.Model):
    category = models.CharField('category', max_length=50)
    subcategory = models.CharField('subcategory', max_length=50)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        unique_together = 'category', 'subcategory',

    def __str__(self):
        return f"{self.category}/{self.subcategory}"
    


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    product_id = models.CharField('Product Id', unique=True, max_length=50)
    product_name = models.CharField('Product Name', max_length=50, blank=True, null=True)
    price = models.CharField('Price$', max_length=50, blank=True, null=True)
    href = models.URLField('Product Link', blank=True, null=True)
    image = models.ImageField('Product Image', upload_to='ecommerce', null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.product_name
