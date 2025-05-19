from django.urls import path

from . import views

app_name = "weather"
urlpatterns = [
    path("display/", views.display, name="display"),
]