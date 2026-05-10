from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
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


# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


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


# Serializer for registering a new user
class RegisterSerializer(serializers.ModelSerializer):
    # Password field
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    # Password Confirmation
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    # Verification usermane
    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required")

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this name exists")

        return value

    # Email field is required
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")

        # Email format check
        EmailValidator()(value)

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")

        return value

    # Password validation
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password mismatch"})

        return attrs

    # Creating a user with a hashed password
    def create(self, validated_data):

        # Delete password2
        validated_data.pop('password2')

        # Create users
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
