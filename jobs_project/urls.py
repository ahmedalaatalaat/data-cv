from django.urls import path
from . import views

app_name = 'jobs_project'

urlpatterns = [
    path("jobs/", views.jobs, name="jobs"),
    path("load_data/", views.load_data_to_database, name="load_data"),
]

