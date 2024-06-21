"""api URL Configuration

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from .views import RegisterUserView, UserLoginAPIView, UserListView, ChangePasswordView, PasswordResetAPIView, \
    PasswordResetConfirmAPIView, CreateProfileAPIView, UpdateUserProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView

# For Auth
auth_url_patterns = [
    path("login/", UserLoginAPIView.as_view(), name="login_user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# For Users
user_url_patterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path("create_user_profile/", CreateProfileAPIView.as_view(), name="get_user_profile"),
    path("update_user_profile/", UpdateUserProfileAPIView.as_view(), name="update_user_profile"),
    path('password/reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmAPIView.as_view(),
         name='password_reset_confirm'),
]

# Concat all url patterns
api_url_patterns = []
api_url_patterns += auth_url_patterns
api_url_patterns += user_url_patterns

urlpatterns = [
    path('v1/', include(api_url_patterns)),
]
