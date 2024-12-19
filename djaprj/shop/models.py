from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
