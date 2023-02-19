from django.urls import path
from . import views

app_name = 'books_project'

urlpatterns = [
    path("books_perspective/", views.books_perspective, name="books_perspective"),
    path("authors_perspective/", views.authors_perspective, name="authors_perspective"),
    path("load_data/", views.load_data_to_database, name="load_data"),
]

