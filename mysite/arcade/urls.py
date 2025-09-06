from django.urls import path
from . import views

app_name = 'arcade'

urlpatterns = [
    path('', views.index, name='index'),
]