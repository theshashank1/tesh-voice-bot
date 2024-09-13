from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('process', views.process, name='process'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

]

