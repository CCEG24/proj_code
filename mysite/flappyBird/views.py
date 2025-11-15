from django.shortcuts import render
from .models import FlappyBirdScore
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def game(request):
    return render(request, 'flappyBird/game.html')

def leaderboard(request):
    # Get all scores, ordered by score descending, then by date
    # Get unique scores by converting to a set of IDs first, then fetching those records
    all_scores = FlappyBirdScore.objects.all().order_by('-score', 'created_at')
    # Get unique score IDs to avoid duplicates
    seen_ids = set()
    unique_scores = []
    for score in all_scores:
        if score.id not in seen_ids:
            seen_ids.add(score.id)
            unique_scores.append(score)
            if len(unique_scores) >= 10:
                break
    
    context = {
        'scores': unique_scores,
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
