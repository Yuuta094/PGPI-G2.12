from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models. password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

class Administrator(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models. password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

