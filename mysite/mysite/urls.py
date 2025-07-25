"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("weather/", include("weather.urls")),
    path("transport/", include("transport.urls")),
    path("", include("home.urls")),  # Add home app at root URL
    path("comments/", include("comments.urls")), # Include the comments app URLs
    path('accounts/', include('accounts.urls')),
    path('forums/', include(('forums.urls', 'forums'), namespace='forums')),
    path('question_bot/', include('question_bot.urls')),
    path('bulletin/', include(('bulletin.urls', 'bulletin'), namespace='bulletin')),
    path('tetris/', include(('tetris.urls', 'tetris'), namespace='tetris')),
]