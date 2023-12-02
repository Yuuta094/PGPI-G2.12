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
    
    path('stillLife/', views.stillLife, name='stillLife'),
    path('portrait/', views.portrait, name='portrait'),
    path('landscape/', views.landscape, name='landscape'),
    path('abstract/', views.abstract, name='abstract'),
    path('figurative/', views.figurative, name='figurative'),
    path('surrealism/', views.surrealism, name='surrealism'),
    path('other/', views.other, name='other'),    
]