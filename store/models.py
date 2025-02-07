from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    description = models.CharField(max_length=200, default='', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    specifications = models.JSONField(blank=True, default=list)
    primary_image = models.ImageField(upload_to='uploads/product/')
    image2 = models.ImageField(upload_to='uploads/product/')
    image3 = models.ImageField(upload_to='uploads/product/')
    image4 = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.product_name

