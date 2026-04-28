from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer

# Task statistics (GET)
@api_view(['GET'])
def task_statistics(request):
    # Total number of tasks
    total_tasks = Task.objects.count()
    # Number of task for each status
    status_breakdown = {}
    for status_code, status_label in Task.Status.choices:
        count = Task.objects.filter(status=status_code).count()
        status_breakdown[status_label] = count

    # Number of overdue tasks
    current_time = timezone.now()
    overdue_tasks = Task.objects.filter(
        deadline__lt=current_time).exclude(
        status=Task.Status.DONE
    ).count()

    return Response({
        'total_tasks': total_tasks,
        'status_breakdown': status_breakdown,
        'overdue_tasks': overdue_tasks,
    })


# GET:list all task, POST:create a new task
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# GET: task by ID, PUT, PATCH, DELETE
class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# GET:list all SubTask, POST:create a new SubTask
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# GET: task by ID, PUT, PATCH, DELETE
class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

