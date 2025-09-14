from django.urls import path
from . import views

app_name = 'flappyBird'

urlpatterns = [
    path('', views.game, name='game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('save-score/', views.save_score, name='save_score'),
]
