from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Token(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="auth_token",
    )
    access_token = models.CharField(
        unique=True,
        max_length=50,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for user {self.user.username}"
