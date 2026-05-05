from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted', 'deleted_at', 'tasks_count']
        read_only_fields = ['id', 'is_deleted', 'deleted_at']

    # Returns the number of tasks associated with this category
    def get_tasks_count(self, obj) -> int:
        return obj.task.count()


# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'owner']
        read_only_fields = ['owner']

# Serializer for creating a SubTask
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


# Serializer for a category with uniqueness checking
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


    # Checking uniqueness when creating
    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError(f"Category named '{name}' already exists.")
        return super().create(validated_data)


    # Checking uniqueness when updating
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and Category.objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError(f"Category named '{name}' already exists.")
        return super().update(instance, validated_data)


# Serializer with nested SubTasks
class SubTaskForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


# Nested serializer to display all SubTasks of a task
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskForTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at', 'subtasks', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


# Validation deadline
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


    # Validation of the deadline field
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past")
        return value

