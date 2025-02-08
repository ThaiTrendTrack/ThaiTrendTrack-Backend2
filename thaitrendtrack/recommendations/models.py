from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=list)
    history = models.JSONField(default=list)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Movie(models.Model):
    title_en = models.CharField(max_length=255)
    title_th = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)  # Make release_date optional
    genres = models.JSONField(default=list)
    description = models.TextField()
    poster_path = models.URLField()
    runtime = models.CharField(max_length=50, blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)  # If you want to store popularity as a float
    vote_average = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title_en
