from django.urls import path
from . import views

app_name = 'mc'

urlpatterns = [
    path('', views.index, name='index'),
]