from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


def login_view(request):
    """Method to manage the custom login logic with JWT"""
    result = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            jwt_token = str(refresh.access_token)
            response = redirect('dashboard')
            response.set_cookie('_uid_token', jwt_token, httponly=True, secure=True)            
            return response
        else:
            result.update({
                "status": 401,
                "msg": "authentication failed.",
                "success": False
            })
            messages.add_message(request, messages.ERROR, 'Invalid credentials, Please try again..')

    return render(request, 'login.html', result)


def logout_view(request):
    """Method to handle the logout functionality along with removing token from cookie.
    """
    response = redirect('/accounts/login/')
    response.delete_cookie('_uid_token', path='/')
    logout(request)
    return response


class UserRegistrationView(generics.CreateAPIView):
    """API view to register a new user."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle user registration."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
           
        
        return Response({
            'status': 'error',
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors,
            'message': 'User registration failed'
        }, status=status.HTTP_400_BAD_REQUEST)
