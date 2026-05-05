from django.db import models
from django.utils import timezone
from django.conf import settings


# Delete
class SoftDeleteManager(models.Manager):
    # Returns only non-deleted entries
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    # Returns all entries, including deleted ones
    def all_with_deleted(self):
        return super().get_queryset()

    # Returns only deleted entries
    def deleted_only(self):
        return super().get_queryset().filter(is_deleted=True)


# Create your models here.
class Category(models.Model):
    # name: category name
    name = models.CharField(max_length=100, unique=True)

    # Soft delete field
    # Is the category deleted?
    is_deleted = models.BooleanField(default=False)
    # When was it deleted?
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def __str__(self) -> str:
        return self.name

    # Soft delete mark as deleted
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    # Restores
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    # contains metadata
    class Meta:
        # name: table
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        PENDING = "PENDING", "Pending"
        BLOCKED = "BLOCKED", "Blocked"
        DONE = "DONE", "Done"

    # title: task title (must be unique for a date)
    title = models.CharField(max_length=200)

    # description: task description
    description = models.TextField()

    # categories: many-to-many relationship with Category
    categories = models.ManyToManyField(Category, related_name="task")

    # status: task status from predefined choices
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    # deadline: date and time of the deadline
    deadline = models.DateTimeField()

    # created_at: automatically stores creation date and time
    created_at = models.DateTimeField(auto_now_add=True)

    # New field task owner
    owner = models.ForeignKey(
        # reference to the User model
        settings.AUTH_USER_MODEL,
        # If a user is deleted all their tasks are also deleted
        on_delete=models.CASCADE,
        # All tasks user
        related_name='tasks',
        # Field can be empty
        null=True,
        # Field can be empty in forms
        blank=True
    )


    def __str__(self) -> str:
        return self.title

    # model settings
    class Meta:
        # database limitations
        constraints = [models.UniqueConstraint(fields=["title", "deadline"], name="unique_task_per_day")]
        db_table = 'task_manager_task'
        # default sorting
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self) -> str:
        return self.title

class SubTask(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        PENDING = "PENDING", "Pending"
        BLOCKED = "BLOCKED", "Blocked"
        DONE = "DONE", "Done"

    # title: subtask title
    title = models.CharField(max_length=200)

    # description: subtask description
    description = models.TextField()

    # task: main task (one-to-many relationship)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")

    # status: subtask status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    # deadline: date and time of the deadline
    deadline = models.DateTimeField()

    # created_at: automatically stores creation date and time
    created_at = models.DateTimeField(auto_now_add=True)

    # New field SubTask owner
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subtasks',
        null=True,
        blank=True
    )

    # model settings
    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
