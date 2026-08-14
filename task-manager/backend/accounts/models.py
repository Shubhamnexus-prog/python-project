from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model so we can extend it later without migration pain."""
    email = models.EmailField(unique=True)
    avatar_color = models.CharField(
        max_length=7,
        default='#6EC6FF',
        help_text='Hex color used for the user avatar chip in the UI.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
