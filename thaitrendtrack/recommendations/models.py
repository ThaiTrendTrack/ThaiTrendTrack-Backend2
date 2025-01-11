from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=list)
    history = models.JSONField(default=list)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

