from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('', views.index, name='index'),  # Home page URL pattern with name 'index'
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),  # Login page URL pattern with name 'login'
]

