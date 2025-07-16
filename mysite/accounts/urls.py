from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('send_verification_code/', views.send_verification_code_view, name='send_verification_code'),
    path('verify_code/', views.verify_code_view, name='verify_code'),
] 