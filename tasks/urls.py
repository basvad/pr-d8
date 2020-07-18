from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("time/", views.time_view, name="time_view"),
    path("list/", views.TaskListView.as_view(), name="list"),
    path("list/c/<slug:cat_slug>", views.tasks_by_cat, name="list_by_cat"),
    path("details/<int:pk>", views.TaskDetailsView.as_view(), name="details"),
]
