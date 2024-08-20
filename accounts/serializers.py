from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Class handles the user registeration"""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'write_only': True},
            'username': {'required': True, 'write_only': True},
            'password': {'required': True, 'write_only': True},
            'confirm_password': {'required': True, 'write_only': True},
        }

    def validate(self, data):
        """Method to add validations"""
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        return data

    def create(self, validated_data):
        """Method to create user after validation"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
