from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from . import views
from .forms import LoginForm


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
]