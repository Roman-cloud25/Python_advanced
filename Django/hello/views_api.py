from rest_framework import status,viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes
import typing
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, SubTask, Category
from .serializers import TaskSerializer, SubTaskCreateSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


# ViewSet for CRUD operations with categories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # Counting tasks in a category
    @action(detail=True, methods=['get'], url_path='count-tasks')
    # Returns the number of tasks in the specified category
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        tasks_count = category.task.count()

        return Response({
            'category_id': category.id,
            'category_name': category.name,
            'tasks_count': tasks_count
        })

    # View deleted categories
    @action(detail=False, methods=['get'], url_path='deleted')
    # Returns a list of only deleted categories
    def deleted_categories(self, request):
        deleted_cats = Category.objects.deleted_only()
        serializer = self.get_serializer(deleted_cats, many=True)
        return Response(serializer.data)

    # Category restoration
    @action(detail=True, methods=['post'], url_path='restore')
    # Restores a soft deleted category
    def restore_category(self, request, pk=None):
        category = Category.objects.all_with_deleted().get(id=pk)
        if not category.is_deleted:
            return Response(
                {'error': 'The category was not deleted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        category.restore()
        serializer = self.get_serializer(category)
        return Response(serializer.data)


# Schema
@extend_schema(
    responses={
        200: {
            'type': 'object',
            'properties': {
                'total_tasks': {'type': 'integer'},
                'status_breakdown': {'type': 'object'},
                'overdue_tasks': {'type': 'integer'},
            }
        }
    }
)


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
        deadline__lt=current_time
    ).exclude(status=Task.Status.DONE).count()

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Automatic installation owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Return only the tasks of the current user
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# GET: task by ID, PUT, PATCH, DELETE
class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Return only the tasks of the  current user
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# GET:list all SubTask, POST:create a new SubTask
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Override
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Override
    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)


# GET: SubTask by ID, PUT, PATCH, DELETE
class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Override
    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

# GET: return all tasks for the current user
@extend_schema(responses=TaskSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-created_at')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# GET: return all SubTask for the current user
@extend_schema(responses=SubTaskCreateSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_subtasks(request):
    subtasks = SubTask.objects.filter(owner=request.user).order_by('-created_at')
    serializer = SubTaskCreateSerializer(subtasks, many=True)
    return Response(serializer.data)