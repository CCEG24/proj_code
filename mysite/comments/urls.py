from django.urls import path
from . import views
 
app_name = 'comments'
urlpatterns = [
    path('', views.comment_wall_view, name='comment_wall'),
] 