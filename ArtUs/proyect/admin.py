from django.contrib import admin
from .models import *

admin.site.register(Artwork)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user']
    # Agrega cualquier otro campo que quieras mostrar en la lista aquí

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['shopping_cart', 'artwork', 'quantity', 'accum_value']
    # Agrega cualquier otro campo que quieras mostrar en la lista aquí

admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItem, CartItemAdmin)

admin.site.register(Order)
admin.site.register(Order_Detail)
admin.site.register(Feedback)
admin.site.register([Customer])
