from django.urls import path
from . import views

app_name = 'tetris'

urlpatterns = [
    path('game/', views.game, name='game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submit_score/', views.submit_score, name='submit_score'),
]