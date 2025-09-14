from django.shortcuts import render
from .models import FlappyBirdScore
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def game(request):
    return render(request, 'flappyBird/game.html')

def leaderboard(request):
    scores = FlappyBirdScore.objects.all()[:10]  # Top 10 scores
    context = {
        'scores': scores,
    }
    return render(request, 'flappyBird/leaderboard.html', context)

@csrf_exempt
@require_POST
def save_score(request):
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', 'Anonymous')
        score = data.get('score', 0)
        
        # Create new score entry
        FlappyBirdScore.objects.create(
            player=request.user if request.user.is_authenticated else None,
            player_name=player_name,
            score=score
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
