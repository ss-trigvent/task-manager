from rest_framework import serializers
from django.contrib.auth.models import User
from tasks.models import Task, TaskMember, TaskComment


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model. Converts Task instances to JSON and vice versa.
    """
    all_users = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()  # Add SerializerMethodField for created_by

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'created_by', 'created_at', 'updated_at', 'all_users']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_all_users(self, obj):
        """
        Retrieve all users in the system.
        """
        users = User.objects.all()
        task_members = TaskMember.objects.filter(task=obj).values_list('member', flat=True)
        non_members = users.exclude(id__in=task_members)
        user_data = [{'id': user.id, 'username': user.username} for user in non_members]
        return user_data
    
    def get_created_by(self, obj):
        """
        Return user detail who created the task.
        """
        user = obj.created_by
        return {
            'id': user.id,
            'username': user.username
        }

class TaskMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskMember model. Handles the serialization of task-member relationships.
    """
    username = serializers.CharField(source='member.username')
    userid = serializers.CharField(source='member.id')
    email = serializers.EmailField(source='member.email')


    class Meta:
        model = TaskMember
        fields = ['id', 'task', 'member','username', 'email', 'userid']
        read_only_fields = ['task', 'member', 'username', 'email', 'userid']

class TaskCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the TaskComment model. Manages the conversion of task comments to and from JSON.
    """
    username = serializers.CharField(source='commented_by.username')


    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'commented_by', 'comment', 'created_at', 'username']
        read_only_fields = ['task','commented_by', 'created_at', 'username']
