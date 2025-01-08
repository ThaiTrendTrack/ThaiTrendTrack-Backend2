# เก็บ databased เป็นเเบบ ORM
# models.py
from django.db import models
from django.contrib.auth.models import User

# ตัวอย่าง Model สำหรับภาพยนตร์
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    poster_path = models.URLField()

    def __str__(self):
        return self.title

# ตัวอย่าง Model สำหรับการกระทำของผู้ใช้ (การดู, การให้คะแนน)
class UserInteraction(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('rate', 'Rate'),
        ('like', 'Like'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    rating = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action_type} {self.movie.title}"

# Model สำหรับการเก็บความชอบ (Genres) ของผู้ใช้
class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} prefers {self.genre}"
