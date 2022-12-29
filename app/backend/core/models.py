"""Database models."""

# Used for typing
from __future__ import annotations

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

class UserManager(BaseUserManager):
    """Manager for system Users."""

    def create_user(
        self, email: str, password: str = None, **extra_fields
    ) -> User:
        """Create, save and return system user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str) -> User:
        """Create, save and return system supersuer/ admin."""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Class for system User."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
