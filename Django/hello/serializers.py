from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category


# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']


# Serializer for creating a SubTask
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']


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
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']


# Nested serializer to display all SubTasks of a task
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskForTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at', 'subtasks']
        read_only_fields = ['id', 'created_at']


# Validation deadline
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'categories', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']


    # Validation of the deadline field
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past")
        return value

