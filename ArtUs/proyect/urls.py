from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from . import views
from .forms import *

app_name = 'proyect'

urlpatterns = [
#Core
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('termsofuse/', views.termsofuse, name='termsofuse'),
#Product
    path('new/', views.new, name='new'),
    path('<int:artwork_id>/edit/',views.edit,name='edit_item'),
    path('<int:artwork_id>/delete_item',views.delete_item , name='delete_item'),
    path('<int:artwork_id>/',views.detail,name='detail'),
    path('search/',views.search_page,name='search_page'),
    path('search/result/',views.search,name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
#Carrito
    path('<int:artwork_id>/add', views.add_shoppingcart_from_product_detail, name='add_from_product_detail'),
    path('<int:artwork_id>/substract', views.substract, name='substract'),
    path('remove/<int:artwork_id>/', views.delete_cart, name='remove'),
    path('subtract/<int:artwork_id>/', views.substract, name='subtract'),
    path('clean/', views.clean, name='clean'),
    path('carrito_detail/', views.carrito_detail, name='carrito_detail'),
    path('<int:artwork_id>/add_cart', views.add_shoppingcart_from_cart, name='add_from_cart'),
    path('subtract/<int:artwork_id>/', views.substract, name='substract'),
    path('delete_cart/<int:artwork_id>/', views.delete_cart, name='delete_cart'),
#Admin
    path('create/', views.create_user, name='create'),
    path('show/', views.show_users, name='show'),
    path('edit/<int:user_id>', views.edit_user, name='edit'),
    path('delete/<int:user_id>', views.destroy_user, name='delete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
#Categorys
    path('stillLife/', views.stillLife, name='stillLife'),
    path('portrait/', views.portrait, name='portrait'),
    path('landscape/', views.landscape, name='landscape'),
    path('abstract/', views.abstract, name='abstract'),
    path('figurative/', views.figurative, name='figurative'),
    path('surrealism/', views.surrealism, name='surrealism'),
    path('other/', views.other, name='other'), 
#Orders
    path('my-order/', views.myOrder, name="my-order"),
    path('select-order/', views.unauthenticatedOrderTrack, name="select-order"),
    path('all-orders/', views.adminOrders, name="all-orders"),
    path('user-order-track/<int:order_id>/', views.userOrderTrack, name="user-order-track"),
    
    path('delete-order/<int:pid>/', views.delete_orders, name="delete_order"),
#FeedBacks
    path('my-feedbacks/', views.my_feedbacks, name="my-feedbacks"),
    path('manage-feedback/', views.manage_feedback, name="manage-feedback"),
    path('user-feedback/<int:order_id>/', views.user_feedback, name="user-feedback"),
    path('delete-feedback/<int:pid>/', views.delete_feedback, name="delete_feedback"),
#Pago
    path('paymentComplete/',views.paymentComplete,name='paymentComplete'),

]