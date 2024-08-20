from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
# from cryptography.fernet import Fernet
from django.contrib.auth.models import User

# key = Fernet.generate_key()
# fernet = Fernet(key)

class JWTAuthMiddleware(MiddlewareMixin):
    """Method to manage the custom login using JWT"""
    def process_request(self, request):
        encrypted_token = request.COOKIES.get("_uid_token")
        if encrypted_token:
            try:
                access_token = AccessToken(encrypted_token)
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                user_id = access_token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
            except:
                return redirect('login')
        else:
            if request.path != '/accounts/login/':
                return redirect('login')
