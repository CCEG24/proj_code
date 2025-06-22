from django.db import models

# Create your models here.
class Answer(models.Model):
    text = models.TextField(max_length=256, unique=True)

class Question(models.Model):
    text = models.TextField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
