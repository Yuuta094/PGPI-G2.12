from django.contrib import admin
from .models import Artwork, Order, Order_Detail


admin.site.register([Artwork, Order_Detail,Order])
