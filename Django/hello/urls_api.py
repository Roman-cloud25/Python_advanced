from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views_api

router = DefaultRouter()
router.register(r'categories', views_api.CategoryViewSet, basename='category')

# Router
urlpatterns = [
    # Registration
    path('register/', views_api.register, name='register'),

    # Login
    path('login/', views_api.login, name='login'),

    # Logout
    path('logout/', views_api.logout, name='logout'),

    # Token update
    path('refresh/', views_api.refresh_token, name='refresh_token'),

    # My Tasks
    path('my-tasks/', views_api.my_tasks, name='my-tasks'),
    path('my-subtasks/', views_api.my_subtasks, name='my-subtasks'),

    # Tasks
    path('tasks/', views_api.task_list, name='task-list'),
    path('tasks/', views_api.create_task, name='create-task'),
    path('tasks/<int:task_id>/', views_api.task_detail, name='task-detail'),

    # SubTasks
    path('subtasks/', views_api.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', views_api.SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),

    # Statistics
    path('tasks/statistics/', views_api.task_statistics, name='task-statistics'),

    # Categories
    path('', include(router.urls)),

]
