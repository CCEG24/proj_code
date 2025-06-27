from . import views
from django.urls import path

urlpatterns = [
    path('upload/', views.bulletin_upload, name='bulletin_upload'),
]