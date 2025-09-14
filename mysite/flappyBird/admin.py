from django.contrib import admin
from .models import FlappyBirdScore

@admin.register(FlappyBirdScore)
class FlappyBirdScoreAdmin(admin.ModelAdmin):
    list_display = ['player_name', 'score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['player_name']
    ordering = ['-score', '-created_at']
