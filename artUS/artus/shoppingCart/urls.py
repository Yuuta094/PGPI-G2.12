from django.urls import path
from . import views

app_name = 'shoppingCart'

urlpatterns = [
    path('add/<int:artwork_id>/', views.add_shoppingcart_from_product_detail, name='add'),
    path('remove/<int:artwork_id>/', views.delete, name='remove'),
    path('subtract/<int:artwork_id>/', views.substract, name='subtract'),
    path('clean/', views.clean, name='clean'),
    path('', views.carrito_detail, name='carrito_detail'),
    path('<int:artwork_id>/add', views.add_shoppingcart_from_cart, name='add_from_cart'),
    path('subtract/<int:artwork_id>/', views.substract, name='substract'),
    path('delete/<int:artwork_id>/', views.delete, name='delete'),
    path('paymentComplete/',views.paymentComplete,name='paymentComplete'),
    path('sucess/',views.sucess,name='sucess'),
]