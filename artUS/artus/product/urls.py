from django.urls import path
from . import views
from shoppingCart.views import add_shoppingcart_from_product_detail,substract

app_name = 'product'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('<int:artwork_id>/edit/',views.edit,name='edit'),
    path('<int:artwork_id>/',views.detail,name='detail'),
    path('search/',views.search_page,name='search_page'),
    path('search/result/',views.search,name='search'),
    path('<int:artwork_id>/delete',views.delete , name='delete'),
    path('carrito/<int:artwork_id>/add', add_shoppingcart_from_product_detail, name='add_from_product_detail'),
    path('<int:artwork_id>/substract', substract, name='substract'),
]