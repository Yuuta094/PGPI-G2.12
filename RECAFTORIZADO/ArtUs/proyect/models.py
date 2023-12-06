from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    telephone = models.CharField(max_length=20, blank=True)


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
    manufacturer = models.CharField(max_length=100)
    opinions = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to='proyect/product_images', null=True, blank=True)


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    accum_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
        
orderStatus = ((1, "Pendiente"), (2, "Enviado"), (3, "En camino"), (4, "Recibido"))

class Order(models.Model):
    ordernum = models.CharField(max_length=9, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=orderStatus, default=1) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    
    address = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
     return self.created.strftime('%b %e %Y %H:%M:%S')


class Order_Detail(models.Model):
    product = models.ForeignKey(Artwork, on_delete= models.CASCADE)
    cant = models.IntegerField()
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.order.customer + ' - ' + self.product.name + ' - ' + str(self.cant) + ' - ' + str(self.order.created)
    

class Feedback(models.Model):
    customer = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.strftime('%b %e %Y %H:%M:%S')