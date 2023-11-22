from django.db import models
from django.contrib.auth.models import User


class Category(models.TextChoices):
    STILL_LIFE = "Still Life"
    PORTRAIT = "Portrait"
    LANDSCAPE = "Landscape"
    ABSTRACT = "Abstract"
    FIGURATIVE = "Figurative"
    SURREALISM = "Surrealism"
    OTHER = "Other"

class Artwork(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=Category.choices, default=Category.PORTRAIT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    opinions = models.JSONField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Order(models.Model):
    ordernum = models.CharField(max_length=9, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True) 

    def __str__(self):
     return self.ordernum
 
class Order_Detail(models.Model):
    product = models.ForeignKey(Artwork, on_delete= models.CASCADE)
    cant = models.IntegerField()
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.product
    
