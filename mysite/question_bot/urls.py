from django.urls import path, include
from . import views

app_name = 'question_bot'

urlpatterns = [
    path('', views.index, name='index'),
    path('question_bot/', include('question_bot.urls')),
]