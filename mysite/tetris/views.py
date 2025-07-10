from django.shortcuts import render
from .models import HighScore
from django.http import JsonResponse

def submit_score(request):
    if request.method == "POST":
        score = int(request.POST.get("score", 0))
        user = request.user if request.user.is_authenticated else None
        HighScore.objects.create(user=user, score=score)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

def leaderboard(request):
    scores = HighScore.objects.order_by('-score')[:10]
    return render(request, 'tetris/leaderboard.html', {'scores': scores})

def game(request):
    return render(request, 'tetris/game.html')