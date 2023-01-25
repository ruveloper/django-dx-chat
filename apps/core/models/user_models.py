from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class User(AbstractUser):
    # Additional fields
    avatar_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        default="",
    )

    def save(self, *args, **kwargs):
        # Set random avatar in case the avatar_url is None
        if not self.avatar_url:
            static_path = f"images/avatars/avatar-{randint(1,12):02d}.svg"
            self.avatar_url = static(static_path)
        super().save(*args, **kwargs)
