from django.urls import path
from . import views

app_name = 'flappyBird'

urlpatterns = [
    path('', views.game, name='game'),
]
