# Import System Modules

# Import Third-party Python Modules
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Import Project Modules
from users.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "role")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = User
        fields = ("username", "email", "password", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(Q(email=data["username"]) | Q(username=data["username"])).first()
        print("user", user)
        if user and user.check_password(data["password"]) and user.is_active:
            return user
        raise ValidationError("Incorrect Credentials", code='authentication_failed')


class ProfileSerializer(UserSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = ("bio", "is_email_verified")


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer class to serialize the change password
    """

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
