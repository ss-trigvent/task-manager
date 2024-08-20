from django.urls import path
from accounts.views import login_view, logout_view, UserRegistrationView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
