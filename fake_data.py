# seed_data.py
import os
import django
from faker import Faker
from django.utils import timezone
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
django.setup()

from django.contrib.auth.models import User
from tasks.models import Task, TaskMember, TaskComment

fake = Faker()

def create_users(num_users):
    users = []
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        users.append(user)
    return users

def create_tasks(users, num_tasks):
    tasks = []
    for _ in range(num_tasks):
        task = Task.objects.create(
            title=fake.sentence(nb_words=3),
            description=fake.text(),
            due_date=fake.date_between(start_date='today', end_date='+30d'),
            created_by=random.choice(users),
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        tasks.append(task)
        
        # Add random members to the task
        num_members = random.randint(1, len(users))  # At least 1 member
        members = random.sample(users, num_members)  # Ensure unique members
        for member in members:
            TaskMember.objects.create(task=task, member=member)

    return tasks

def create_comments(tasks, num_comments, users):
    comments_created = 0
    while comments_created < num_comments:
        task = random.choice(tasks)
        user = random.choice(users)
        if TaskComment.objects.filter(task=task, commented_by=user).count() < 5:  # limit comments per user per task
            TaskComment.objects.create(
                task=task,
                commented_by=user,
                comment=fake.sentence(),
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
            comments_created += 1

if __name__ == "__main__":
    num_users = 5
    num_tasks = 10
    num_comments = 20

    # Create users
    users = create_users(num_users)
    print(f"Created {num_users} users.")

    # Create tasks
    tasks = create_tasks(users, num_tasks)
    print(f"Created {num_tasks} tasks.")

    # Create comments
    create_comments(tasks, num_comments, users)
    print(f"Created {num_comments} comments.")
