from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('<int:pk>/delete/',views.delete,name='delete'),
    path('<int:pk>/edit/',views.delete,name='edit'),
    path('<int:pk>/',views.detail,name='detail'),

]