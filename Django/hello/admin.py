from django.contrib import admin
from .models import Task, SubTask, Category

from django.contrib import admin
from .models import Task, SubTask, Category

# Administrator class Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Show ID and name
    list_display = ('id', 'name')

    # Click
    list_display_links = ('id', 'name')

    # Search
    search_fields = ('name',)

    # Sort by alphabet
    ordering = ('name',)


# Administrator class Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Show
    list_display = ('id', 'title', 'status', 'deadline', 'created_at')

    # Click
    list_display_links = ('id', 'title')

    # Search
    search_fields = ('title', 'description')

    # Filter
    list_filter = ('status', 'categories', 'deadline')

    # Edit
    list_editable = ('status',)

    # Read
    readonly_fields = ('created_at',)

    # Edit
    fieldsets = (
        ('Basic information', {
            'fields': ('title', 'description', 'categories')
        }),
        ('Status and deadline', {
            'fields': ('status', 'deadline')
        }),
        ('System information', {
            'fields': ('created_at',),
            # Roll-up
            'classes': ('collapse',)
        }),
    )

    # Default sorting
    ordering = ('-created_at',)


# Administrator class SubTask
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Show
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')

    # Click
    list_display_links = ('id', 'title')

    # Search
    search_fields = ('title', 'description', 'task__title')  # task__title - поиск по задаче

    # Filter
    list_filter = ('status', 'task', 'deadline')

    # Edit
    list_editable = ('status',)

    # Read
    readonly_fields = ('created_at',)

    # Default sorting
    ordering = ('-created_at',)