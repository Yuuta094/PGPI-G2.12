from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
