# messaging_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserMessageViewSet

router = DefaultRouter()
router.register(r'messages', UserMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
