from django.contrib import admin
from .models import TowerGameScore

@admin.register(TowerGameScore)
class TowerGameScoreAdmin(admin.ModelAdmin):
	list_display = ["player_name", "moves", "difficulty", "created_at"]
	list_filter = ["difficulty", "created_at"]
	search_fields = ["player_name"]
	ordering = ["moves", "-difficulty", "created_at"]