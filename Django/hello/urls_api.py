from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views_api


# Router for categories
router = DefaultRouter()
router.register(r'categories', views_api.CategoryViewSet, basename='category')

# Router
urlpatterns = [
    # JWT getting and updating the token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена

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