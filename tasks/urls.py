from django.urls import path
from .views import (
    TaskDelete,
    TasksView,
    TaskView,
    TasksCreateView,
    TasksEditView,
    PriorityTasksView,
    IndexView,
    SearchTasksView,
)

urlpatterns = [
    path("", IndexView.as_view()),
    path("tasks/", TasksView.as_view(), name="home"),
    path("tasks/search/", SearchTasksView.as_view(), name="search"),
    path("tasks/priorities/", PriorityTasksView.as_view(), name="priorities"),
    path("tasks/create/", TasksCreateView.as_view(), name="create"),
    path("task/<int:pk>/", TaskView.as_view(), name="task"),
    path("task/edit/<int:pk>/", TasksEditView.as_view(), name="edit"),
    path("task/delete/<int:pk>/", TaskDelete.as_view(), name="delete"),
]
