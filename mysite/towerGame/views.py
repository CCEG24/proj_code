from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import TowerGameScore


# Create your views here.
def index(request):
    return render(request, 'towerGame/game.html')


def leaderboard(request):
    scores = TowerGameScore.objects.all()
    score_rows = []

    for score in scores:
        optimal_moves = (2 ** score.difficulty) - 1
        wasted_moves = max(0, score.moves - optimal_moves)
        score_rows.append(
            {
                "id": score.id,
                "player_name": score.player_name,
                "moves": score.moves,
                "difficulty": score.difficulty,
                "optimal_moves": optimal_moves,
                "wasted_moves": wasted_moves,
                "created_at": score.created_at,
            }
        )

    # Keep ranking aligned with displayed values instead of relying on stored wasted_moves.
    score_rows.sort(
        key=lambda row: (
            row["wasted_moves"],
            row["moves"],
            -row["difficulty"],
            row["created_at"],
        )
    )

    return render(request, 'towerGame/leaderboard.html', {'scores': score_rows})


@require_http_methods(["POST"])
def submit_score(request):
    import json
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', 'Anonymous').strip()[:100]
        moves = int(data.get('moves', 0))
        difficulty = int(data.get('difficulty', 3))
        
        if moves < 0 or difficulty < 1 or difficulty > 8:
            return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)

        optimal_moves = (2 ** difficulty) - 1
        wasted_moves = max(0, moves - optimal_moves)
        
        score = TowerGameScore.objects.create(
            player_name=player_name,
            moves=moves,
            difficulty=difficulty,
            wasted_moves=wasted_moves,
        )
        
        return JsonResponse({
            'success': True,
            'score_id': score.id,
            'message': f'Score saved! Your rank: {score.id}'
        })
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
