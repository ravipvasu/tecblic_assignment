# Import System Modules

# Import Third-party Python Modules
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

# Import Project Modules

User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_ADMIN


class IsSolutionProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_SOLUTION_PROVIDER


class IsSolutionSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_SOLUTION_SEEKER
