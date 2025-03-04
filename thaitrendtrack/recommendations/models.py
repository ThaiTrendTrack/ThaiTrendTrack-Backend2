from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=list)
    history = models.JSONField(default=list)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# class Movie(models.Model):
#     title_en = models.CharField(max_length=255)
#     title_th = models.CharField(max_length=255, blank=True, null=True)
#     release_date = models.DateField(null=True, blank=True)  # Make release_date optional
#     genres = models.JSONField(default=list)
#     description = models.TextField()
#     poster_path = models.URLField()
#     runtime = models.CharField(max_length=50, blank=True, null=True)
#     popularity = models.FloatField(blank=True, null=True)  # If you want to store popularity as a float
#     vote_average = models.FloatField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title_en

from django.db import models
import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# ✅ Load BERT Model (Multilingual for Thai Support)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModel.from_pretrained("bert-base-multilingual-cased")
model.eval()


def get_bert_embedding(text):
    """Generate BERT embeddings for Thai & English text."""
    if not text or text.strip() == "":
        return np.zeros((1, 768)).tolist()  # ✅ Return zero vector if no text

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy().reshape(1, -1).tolist()  # ✅ Ensure correct format


class Movie(models.Model):
    title_en = models.CharField(max_length=255)
    title_th = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    poster_path = models.URLField()
    genres = models.JSONField(default=list)
    runtime = models.CharField(max_length=50, blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)  # If you want to store popularity as a float
    vote_average = models.FloatField(blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)  # ✅ Store embeddings as JSON

    def save(self, *args, **kwargs):
        """Force embedding creation when saving a movie."""
        if not self.embedding and self.description:  # ✅ Only generate if it's missing
            print(f"Generating embedding for: {self.title_en}")  # ✅ Debug log
            embedding_vector = get_bert_embedding(self.description)
            self.embedding = json.dumps(embedding_vector)  # ✅ Store JSON format
        super().save(*args, **kwargs)  # ✅ Call Django's original save()
