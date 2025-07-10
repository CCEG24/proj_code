from django.shortcuts import render
from .models import HighScore

def leaderboard(request):
    scores = HighScore.objects.order_by('-score')[:10]
    return render(request, 'tetris/leaderboard.html', {'scores': scores})

def game(request):
    return render(request, 'tetris/game.html')