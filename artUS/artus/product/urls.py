from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('<int:pk>/delete/',views.delete,name='delete'),
    path('<int:pk>/edit/',views.edit,name='edit'),
    path('<int:pk>/',views.detail,name='detail'),
    path('search/',views.search_page,name='search_page'),
    path('search/result/',views.search,name='search'),
    path('new/#',views.simple_checkout,name='simple_checkout'), #TODO cambiar 
    path('sucess/',views.sucess,name='sucess'),
    
    
]