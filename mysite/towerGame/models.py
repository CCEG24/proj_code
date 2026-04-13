from django.db import models

# Create your models here.
class TowerGameScore(models.Model):
    player_name = models.CharField(max_length=100, default="Anonymous")
    moves = models.IntegerField()
    difficulty = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['moves', 'difficulty']
        verbose_name = "Tower Game Score"
        verbose_name_plural = "Tower Game Scores"
    
    def __str__(self):
        return f"{self.player_name}: {self.moves} moves (difficulty {self.difficulty})"