from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import Task, SubTask, Category
from .serializers import TaskSerializer, SubTaskCreateSerializer, CategorySerializer


# Generic Views for Task
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# Endpoint for retrieving, updating or deleting a task instance
class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Task list with filtering by day of the week
@api_view(['GET'])
def task_list(request):
    weekday_param = request.query_params.get('weekday')
    tasks = Task.objects.all()

    if weekday_param:
        weekday_number = _get_weekday_number(weekday_param)
        if weekday_number:
            tasks = tasks.filter(deadline__week_day=weekday_number)

    tasks = tasks.order_by('-created_at')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# Day of the week name into number
def _get_weekday_number(weekday_name):
    weekdays = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7
    }
    return weekdays.get(weekday_name.lower(), None)


# Pagination of more than 5 objects
class SubTaskListCreateView(APIView):
    def get(self, request):
        page_size = 5
        page_number = request.query_params.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        task_title = request.query_params.get('task_title')
        status_filter = request.query_params.get('status')
        subtasks = SubTask.objects.all()
        if task_title:
            subtasks = subtasks.filter(task_title_icontains=task_title)
        if status_filter:
            subtasks = subtasks.filter(status=status_filter)
        subtasks = subtasks.order_by('-created_at')

        paginator = Paginator(subtasks, page_size)
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return Response({
                'count': paginator.count,
                'page': page_number,
                'total_pages': paginator.num_pages,
                'results': []
            })

        serializer = SubTaskCreateSerializer(page_obj, many=True)
        return Response({
            'count': paginator.count,
            'page': page_number,
            'total_pages': paginator.num_pages,
            'results': serializer.data
        })

    # Creating a new SubTask
    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# POST
@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Created object in JSON
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
    # Information is not valid
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


# ID GET
@api_view(['GET'])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise NotFound(f"Task with ID {task_id} not found")

    # Serialize the task to JSON
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


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


# Update, Delete SubTask
class SubTaskDetailUpdateDeleteView(APIView):
    # Find SubTask
    def get_object(self, pk):
        try:
            return SubTask.objects.get(id=pk)
        except SubTask.DoesNotExist:
            raise NotFound("Subtask not found")

    # GET: SubTask
    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update SubTask
    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial SubTask update
    def patch(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: delete SubTask
    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Registering a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # Passing request data to the serializer
    serializer = RegisterSerializer(data=request.data)

    # Validate data
    if serializer.is_valid():
        # Saving the user
        user = serializer.save()

        # Answer
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User successfully registered'
        }, status=status.HTTP_201_CREATED)

    # Return errors on validation failure
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Data from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # Validation: username and password are required
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # User Aunthentication
    user = authenticate(username=username, password=password)

    # Validate user existens and password
    if user is None:
        return Response({
            'error': 'Incorrect username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Create JWT Token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Reply
    response = Response({
        'message': 'Login successful',
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_200_OK)

    # Setting the access token in an HttpOnly cookie
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,  # XSS protection
        samesite='Lax',
        max_age=1800,
    )

    # Setting the refresh token in an HttpOnly cookie
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='Lax',
        max_age=86400,
    )
    return response


# Access Token Refresh
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({
            'error': 'Refresh токен не найден'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        # Creating a response
        response = Response({
            'message': 'Access Token updated'
        }, status=status.HTTP_200_OK)

        # Setting the new access token in a cookie
        response.set_cookie(
            key='access_token',
            value=new_access_token,
            httponly=True,
            samesite='Lax',
            max_age=1800,
        )
        return response

    except Exception as e:
        return Response({
            'error': 'Invalid refresh Token'
        }, status=status.HTTP_401_UNAUTHORIZED)


# My Tasks
@api_view(['GET'])
def my_tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-created_at')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# Returns all SubTask of the current user
@api_view(['GET'])
def my_subtasks(request):
    subtasks = SubTask.objects.filter(owner=request.user).order_by('-created_at')
    serializer = SubTaskCreateSerializer(subtasks, many=True)
    return Response(serializer.data)


# Logout
@api_view(['POST'])
def logout(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except TokenError:
            pass

    # Creating response
    response = Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


# ViewSet for CRUD
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
