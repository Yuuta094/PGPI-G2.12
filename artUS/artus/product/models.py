from django.db import models

class Category(models.TextChoices):
    NATURALEZA_MUERTA = "Naturaleza muerta"
    RETRATO = "Retrato"
    PAISAJE = "Paisaje"
    ABSTRACTO = "Abstracto"
    FIGURATIVO = "Figurativo"

class Obra(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=Category.choices, default=Category.NATURALEZA_MUERTA)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    opinions = models.JSONField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
