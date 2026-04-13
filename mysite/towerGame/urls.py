from django.urls import path
from . import views

app_name = 'towerGame'

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submit_score/', views.submit_score, name='submit_score'),
]