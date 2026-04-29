from django.urls import path, include
from . import views_api
from rest_framework.routers import DefaultRouter

# Router for categories
router = DefaultRouter()
router.register(r'categories', views_api.CategoryViewSet, basename='category')

# Router
urlpatterns = [
    # Tasks
    path('tasks/', views_api.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views_api.TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),

    # SubTask
    path('subtasks/', views_api.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', views_api.SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),

    # Statistics
    path('tasks/statistics/', views_api.task_statistics, name='task-statistics'),

]

urlpatterns += router.urls