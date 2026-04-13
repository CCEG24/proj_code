from django.contrib import admin
from .models import HighScore

@admin.register(HighScore)
class HighScoreAdmin(admin.ModelAdmin):
	list_display = ["user", "score", "date"]
	list_filter = ["date"]
	search_fields = ["user__username"]
	ordering = ["-score", "date"]
