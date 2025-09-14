from django.db import models
from django.contrib.auth.models import User

class FlappyBirdScore(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    player_name = models.CharField(max_length=100, default="Anonymous")
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', 'created_at']  # Highest scores first, then by date
        verbose_name = "Flappy Bird Score"
        verbose_name_plural = "Flappy Bird Scores"
    
    def __str__(self):
        return f"{self.player_name}: {self.score} points"
