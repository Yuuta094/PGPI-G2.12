from django.urls import path
from . import views

app_name = 'shoppingCart'

urlpatterns = [
    path('add/<int:artwork_id>/', views.add_shoppingcart_from_product_detail, name='add_cart'),
    path('remove/<int:artwork_id>/', views.delete, name='remove'),
    path('clean/', views.clean, name='clean'),
    path('', views.carrito_detail, name='carrito_detail'),
    path('<int:artwork_id>/add', views.add_shoppingcart_from_cart, name='add_from_cart'),
    path('subtract/<int:artwork_id>/', views.substract, name='substract'),
]