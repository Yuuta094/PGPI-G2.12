from django.urls import path
from . import views
from shoppingCart.views import add_shoppingcart_from_product_detail,delete,substract,clean

app_name = 'product'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('<int:artwork_id>/edit/',views.edit,name='edit'),
    path('<int:artwork_id>/',views.detail,name='detail'),
    path('search/',views.search_page,name='search_page'),
    path('search/result/',views.search,name='search'),
    path('carrito/<int:artwork_id>/add', add_shoppingcart_from_product_detail, name='add_from_product_detail'),
    path('<int:artwork_id>/delete',delete , name='delete'),
    path('<int:artwork_id>/substract', substract, name='substract'),
    path('simple_checkout/',views.simple_checkout,name='simple_checkout'), #TODO cambiar 
    path('paymentComplete/',views.paymentComplete,name='paymentComplete'),
    path('sucess/',views.sucess,name='sucess'),
    
    
]