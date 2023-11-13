from django.urls import path
from . import views
app_name = 'product'
urlpatterns = [
    path('<int:pk>/',views.detail,name='detail'),
    path('search/',views.search_page,name='search_page'),
    path('search/result/',views.search,name='search'),
]
