from django.urls import path
from tasks.views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskDetailView, AddTaskMembersView, RemoveTaskMembersView,
    TaskMembersView, AddCommentView, TaskCommentsListView, TaskCommentDeleteView
)

urlpatterns = [
    # Urls to manage the tasks
    path('', TaskListView.as_view(), name='list_tasks'),
    path('<int:pk>/', TaskDetailView.as_view(), name='retrieve_task'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    
    # Urls to manage the Task users
    path('<int:task_id>/members/', TaskMembersView.as_view(), name='list_task_members'),
    path('<int:task_id>/members/add/', AddTaskMembersView.as_view(), name='add_task_members'),
    path('<int:task_id>/members/remove/', RemoveTaskMembersView.as_view(), name='remove_task_members'),
    
    #Urls to manage comments based on tasks    
    path('<int:task_id>/comments/', TaskCommentsListView.as_view(), name='list_comments'),
    path('<int:task_id>/comments/add/', AddCommentView.as_view(), name='create_comment'),
    path('<int:task_id>/comments/<int:comment_id>/delete/', TaskCommentDeleteView.as_view(), name='task-comment-delete'),
]
