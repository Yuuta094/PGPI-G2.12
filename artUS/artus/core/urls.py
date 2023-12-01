from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from . import views
from .forms import LoginForm
from .views import edit_profile

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_user, name='create'),
    path('show/', views.show_users, name='show'),
    path('edit/<int:user_id>', views.edit_user, name='edit'),
    path('delete/<int:user_id>', views.destroy_user, name='delete'),
     path('edit_profile/', edit_profile, name='edit_profile'),

]