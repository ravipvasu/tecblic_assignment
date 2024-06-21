# Import System Modules


from django.db import models
from django.contrib.auth.models import AbstractUser

from rbac_api.settings import AUTH_USER_MODEL
from .managers import CustomUserManager


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_SOLUTION_PROVIDER = 'solution_provider'
    ROLE_SOLUTION_SEEKER = 'solution_seeker'

    ROLES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SOLUTION_PROVIDER, 'Solution Provider'),
        (ROLE_SOLUTION_SEEKER, 'Solution Seeker'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default=ROLE_SOLUTION_SEEKER, db_default=ROLE_SOLUTION_SEEKER)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class Base(models.Model):
    is_active = models.SmallIntegerField(default=1, db_default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)
    param_varchar_1 = models.CharField(max_length=255, blank=True, null=True)
    param_varchar_2 = models.CharField(max_length=255, blank=True, null=True)
    param_varchar_3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class Profile(Base):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="user_profile")
    is_email_verified = models.SmallIntegerField(default=0, db_default=0)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.email
