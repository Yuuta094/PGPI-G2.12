from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from product.models import Artwork

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    accum_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    
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