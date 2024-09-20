import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True)
    is_test = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    @staticmethod
    def camel_to_snake(s):
        return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email,
                    password=None, is_active=True, is_admin=False,
                    is_staff=False):
        if not first_name:
            raise ValueError("User must have a first name")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must specify password")
        user_obj = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save()
        return user_obj

    def create_staff(self, first_name, email, password=None, username=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password,
            is_staff=True
        )

        return user

    def create_superuser(
            self, username, first_name,
            email, password=None
    ):
        user = self.create_user(
            username,
            first_name,
            email,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model representing a user with authentication-related fields.
    The User model defines fields for user authentication and profile information, including
    username, email, password, and user roles.
    """
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=30)

    last_name = models.CharField(
        max_length=30, null=True, blank=True
    )

    username = models.CharField(
        unique=True, max_length=60,
        blank=True, null=True
    )
    email = models.EmailField(unique=True, max_length=60)
    email_verified = models.BooleanField(default=False)

    # password field
    password = models.CharField(blank=True, max_length=500, null=True)
    password_last_updated = models.DateTimeField(blank=True, null=True, default=timezone.now)

    last_login = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True)
    is_test = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'password']
    objects = UserManager()

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.admin
