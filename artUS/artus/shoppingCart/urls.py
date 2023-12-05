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
    path('delete/<int:artwork_id>/', views.delete, name='delete'),
    
    
    
    
    
    #----------------------#
    path('my-order/', views.myOrder, name="my-order"),
    path('my-feedbacks/', views.my_feedbacks, name="my-feedbacks"),
    path('paymentComplete/',views.paymentComplete,name='paymentComplete'),
    path('select-order/', views.unauthenticatedOrderTrack, name="select-order"),
    path('all-orders/', views.adminOrders, name="all-orders"),
    path('manage-feedback/', views.manage_feedback, name="manage-feedback"),
    path('user-feedback/<int:order_id>/', views.user_feedback, name="user-feedback"),
    path('delete-feedback/<int:pid>/', views.delete_feedback, name="delete_feedback"),
    path('user-order-track/<int:order_id>/', views.userOrderTrack, name="user-order-track"),
    path('delete-order/<int:pid>/', views.delete_orders, name="delete_order"),
    #----------------------#
    

    
    
]