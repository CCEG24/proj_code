from django.urls import path
from . import views

app_name = 'towerGame'

urlpatterns = [
    path('', views.index, name='index'),
]