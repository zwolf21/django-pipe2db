# Generated by Django 3.2.6 on 2021-08-20 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, verbose_name='category')),
                ('subcategory', models.CharField(max_length=50, verbose_name='subcategory')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
                'unique_together': {('category', 'subcategory')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=50, unique=True, verbose_name='Product Id')),
                ('product_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Product Name')),
                ('price', models.CharField(blank=True, max_length=50, null=True, verbose_name='Price$')),
                ('href', models.URLField(blank=True, null=True, verbose_name='Product Link')),
                ('image', models.ImageField(null=True, upload_to='ecommerce', verbose_name='Product Image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
    ]
