from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """Model representing a task created by a user.
    """
    STATUS_CHOICES = [
        ('Todo', 'Todo'),
        ('Inprogress', 'Inprogress'),
        ("Complete", 'Complete'),
        ("NotRequired", 'Not Required')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Todo')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class TaskMember(models.Model):
    """Model representing a relationship between a task and its members.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'member')

class TaskComment(models.Model):
    """Model representing a comment on a task."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
