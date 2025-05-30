from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),
    path('new/', views.create_thread, name='create_thread'),
] 