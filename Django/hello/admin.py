from django.contrib import admin
from django.utils.html import format_html
from .models import Task, SubTask, Category


# Inline class for subtasks
class SubTaskInline(admin.TabularInline):
    model = SubTask
    # Show 2 blank lines to add
    fields = ('title', 'description', 'status', 'deadline')
    readonly_fields = ('created_at',)
    can_delete = True
    # Default sorting
    ordering = ('-created_at',)


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
    # Abbreviated name
    def short_title(self, obj):
        max_length = 10
        if len(obj.title) > max_length:
            short = f"{obj.title[:max_length]}"
            return format_html('<span title="{}">{}</span', obj.title, short)
        return obj.title

    short_title.short_description = "Task name abbreviated"

    # Show
    list_display = ('id', 'short_title', 'status', 'deadline', 'created_at')

    # Click
    list_display_links = ('id', 'short_title')

    # Search
    search_fields = ('short_title', 'description')

    # Filter
    list_filter = ('status', 'categories', 'deadline')

    # Edit
    list_editable = ('status',)

    # Read
    readonly_fields = ('created_at',)

    # Inline forms for SubTasks
    inlines = [SubTaskInline]

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

    # List of available actions
    actions = ['mark_as_done']

    # Status changes to Done
    def mark_as_done(self, request, queryset):
        count = queryset.update(status=SubTask.Status.DONE)
        self.massage_user(
            request,
            f"Status changed to 'Done' for {count} SubTasks"
        )

    # Setting the text in a drop-down list
    mark_as_done.short_description = f"Change the status of the selected SubTask to 'Done'"
