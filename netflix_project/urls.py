from django.urls import path
from . import views

app_name = 'netflix_project'

urlpatterns = [
    path("netflix_titles/", views.netflix_titles, name="netflix_titles"),
]

