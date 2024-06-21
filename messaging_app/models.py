# Import System Modules

# Import Third-party Python Modules
from django.db import models

# Import Project Modules
from rbac_api.settings import AUTH_USER_MODEL


class UserMessage(models.Model):
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
