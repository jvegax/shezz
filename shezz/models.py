from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    price_discount = models.FloatField()
    price_original = models.FloatField()
    category = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    product_link = models.URLField()
    sizes = models.CharField(max_length=50)
    images = models.URLField()
    currency = models.CharField(max_length=50)
