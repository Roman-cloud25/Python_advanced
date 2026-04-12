from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer




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


# GET
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    # Serializing a task list to JSON
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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


# List of SubTasks
class SubTaskListCreateView(APIView):
    # GET: list of all SubTasks
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: create a new Subtask
    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        subtask=self.get_object(pk)
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































