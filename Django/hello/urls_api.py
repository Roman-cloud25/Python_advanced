from django.urls import path
from . import views_api

# Router
urlpatterns = [
    # GET: list tasks
    path('tasks/', views_api.task_list, name='api-task-list'),

    # POST: create a task
    path('tasks/', views_api.create_task, name='api-create-task'),

    # GET: statistics
    path('tasks/statistics/', views_api.task_statistics, name='api-task-statistics'),

    # GET: task by ID
    path('tasks/<int:task_id>/', views_api.task_detail, name='api-task-detail'),

    # GET: list SubTask, POST create SubTask
    path('subtasks/', views_api.SubTaskListCreateView.as_view(), name='subtask-list-create'),

    # GET, PUT, PATCH, DELETE: working with one SubTask
    path('subtasks/<int:pk>/', views_api.SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),


]
