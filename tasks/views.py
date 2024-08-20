from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.response import Response
from tasks.models import Task, TaskMember, TaskComment
from tasks.serializers import TaskSerializer, TaskMemberSerializer, TaskCommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.contrib.auth.models import User


class TaskListView(generics.ListAPIView):
    """API view to list all tasks."""
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        """
        Return the tasks assigned to the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        
        assigned_tasks = TaskMember.objects.filter(member=user).values_list('task', flat=True)
        created_tasks = Task.objects.filter(created_by=user).values_list('id', flat=True)
        all_task_ids = set(assigned_tasks) | set(created_tasks)

        return Task.objects.filter(id__in=all_task_ids)

    
    def list(self, request, *args, **kwargs):
        """Retrieve a list of all posts with pagination.
        """
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_at'))
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Tasks retrieved successfully'
        }, status=status.HTTP_200_OK)
        

class TaskCreateView(generics.CreateAPIView):
    """API view to create a new task."""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        """Handle POST request to create a new task."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'data': serializer.data,
                'message': 'Task created successfully'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'errors': str(e),
                'message': 'Failed to create task'
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateView(generics.UpdateAPIView):
    """API view to update an existing task."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        """Handle PATCH request to update an existing task."""
        try:
            task = self.get_object()
            serializer = self.get_serializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_200_OK,
                'data': serializer.data,
                'message': 'Task updated successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'errors': str(e),
                'message': 'Failed to update task'
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(generics.DestroyAPIView):
    """API view to delete a task."""
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs):
        """Handle DELETE request to delete a task."""
        try:
            task = self.get_object()
            task.delete()
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_204_NO_CONTENT,
                'message': 'Task deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'errors': str(e),
                'message': 'Failed to delete task'
            }, status=status.HTTP_404_NOT_FOUND)


class TaskDetailView(generics.RetrieveAPIView):
    """API view to retrieve details of a single task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        """Retrieve a single task by ID."""
        try:
            return super().get(request, *args, **kwargs)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)


class TaskMembersView(APIView):
    """API view to list all members of a specific task."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, task_id, *args, **kwargs):
        """Retrieve all members of a specific task."""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

        task_members = TaskMember.objects.filter(task=task)
        serializer = TaskMemberSerializer(task_members, many=True)

        return Response({
            'status': 'success',
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Members retrieved successfully'
        }, status=status.HTTP_200_OK)

class AddTaskMembersView(APIView):
    """API view to add a single member to a task."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, task_id, *args, **kwargs):
        """Add a specific member to a task."""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

        member_id = request.data.get('member_id')
        if not member_id:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'Member ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=member_id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        if TaskMember.objects.filter(task=task, member=user).exists():
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'User is already a member of this task'
            }, status=status.HTTP_400_BAD_REQUEST)

        TaskMember.objects.create(task=task, member=user)

        return Response({
            'status': 'success',
            'statusCode': status.HTTP_201_CREATED,
            'message': 'Member added successfully'
        }, status=status.HTTP_201_CREATED)


class RemoveTaskMembersView(APIView):
    """API view to remove members from a task."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, task_id, *args, **kwargs):
        """Remove a specific member from a task."""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

        member_id = request.data.get('member_id')
        if not member_id:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'Member ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=member_id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        task_member = TaskMember.objects.filter(task=task, member=user).first()
        if not task_member:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'User is not a member of this task'
            }, status=status.HTTP_404_NOT_FOUND)

        task_member.delete()

        return Response({
            'status': 'success',
            'statusCode': status.HTTP_200_OK,
            'message': 'Member removed successfully'
        }, status=status.HTTP_200_OK)


class TaskCommentsListView(generics.ListAPIView):
    """API view to list all comments for a specific task."""

    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return comments for the specific task."""
        task_id = self.kwargs.get('task_id')
        return TaskComment.objects.filter(task_id=task_id)

    def get(self, request, *args, **kwargs):
        """Retrieve all comments for a specific task with pagination."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Comments retrieved successfully'
        }, status=status.HTTP_200_OK)


class AddCommentView(APIView):
    """API view to add a comment to a specific task."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, task_id, *args, **kwargs):
        """Add a comment to a specific task."""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Create a new comment
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, commented_by=request.user)
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'data': serializer.data,
                'message': 'Comment added successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
            'message': 'Invalid data'
        }, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentDeleteView(generics.DestroyAPIView):
    """API view to delete a specific comment."""

    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """Delete a comment by its ID."""
        comment_id = self.kwargs.get('comment_id')
        try:
            comment = self.get_queryset().get(id=comment_id)
            self.perform_destroy(comment)
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_204_NO_CONTENT,
                'message': 'Comment deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except TaskComment.DoesNotExist:
            return Response({
                'status': 'error',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'message': 'Comment not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        """Delete the comment instance."""
        instance.delete()
