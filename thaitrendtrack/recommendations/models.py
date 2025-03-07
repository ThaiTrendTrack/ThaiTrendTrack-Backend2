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


# from django.db import models
# import json
# import numpy as np
# from transformers import AutoTokenizer, AutoModel
# import torch
#
# # ✅ Load BERT Model
# tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
# model = AutoModel.from_pretrained("bert-base-multilingual-cased")
# model.eval()
#
#
# def get_bert_embedding(text):
#     """Generate BERT embeddings with extra information for diversity."""
#     if not text or text.strip() == "":
#         return np.zeros((1, 768)).tolist()
#
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).numpy().reshape(1, -1).tolist()
#
#
# class Movie(models.Model):
#     title_en = models.CharField(max_length=255)
#     title_th = models.CharField(max_length=255, blank=True, null=True)
#     release_date = models.DateField(null=True, blank=True)
#     description = models.TextField()
#     poster_path = models.URLField()
#     genres = models.JSONField(default=list)
#     runtime = models.CharField(max_length=50, blank=True, null=True)
#     popularity = models.FloatField(blank=True, null=True)
#     vote_average = models.FloatField(blank=True, null=True)
#     embedding = models.TextField(blank=True, null=True)
#
#     def save(self, *args, **kwargs):
#         """Generate more diverse embeddings using extra keywords."""
#         if not self.embedding:
#             genre_keywords = {
#                 "โรแมนติก": "รัก หวาน คู่รัก จูบ ความสัมพันธ์ อบอุ่น แฟน ความรัก",
#                 "ตลก": "ตลก ขำขัน ฮาๆ สนุก คอมเมดี้ เบาสมอง ฮาไม่ไหว",
#                 "แอคชั่น": "แอคชั่น ต่อสู้ ยิง ระเบิด ตื่นเต้น ลุ้น",
#                 "ดราม่า": "เศร้า เสียน้ำตา เรื่องจริง ละครชีวิต",
#                 "สยองขวัญ": "ผี หลอน ฆาตกรรม น่ากลัว มืดมน"
#             }
#
#             # ✅ Add more weight to genres
#             genre_text = " ".join(self.genres)
#             for genre in self.genres:
#                 if genre in genre_keywords:
#                     genre_text += " " + genre_keywords[genre]
#
#             # ✅ Add unique text for each movie to reduce duplicates
#             unique_text = f"ID: {self.id} Popularity: {self.popularity} Vote: {self.vote_average}"
#
#             combined_text = f"{self.title_en} {self.title_th} {genre_text} {self.description} {unique_text}"
#             print(f"🔄 Generating diverse embedding for: {self.title_en}")
#
#             embedding_vector = get_bert_embedding(combined_text)
#             self.embedding = json.dumps(embedding_vector)
#         super().save(*args, **kwargs)

from django.db import models
import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# ✅ Load BERT Model (for embeddings)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModel.from_pretrained("bert-base-multilingual-cased")
model.eval()

def get_bert_embedding(text):
    """Generate BERT embeddings."""
    if not text or text.strip() == "":
        return np.zeros((1, 768)).tolist()

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy().tolist()[0]  # Convert to list

class Movie(models.Model):
    id = models.AutoField(primary_key=True)  # ✅ Matches `id` column in CSV
    title_th = models.CharField(max_length=255, blank=True, null=True)  # ✅ Matches `thai_title`
    title_en = models.CharField(max_length=255, blank=True, null=True)  # ✅ Matches `english_title`
    original_title = models.CharField(max_length=255, blank=True, null=True)  # ✅ Matches `original_title`
    genres = models.JSONField(default=list)  # ✅ Corrected
    status = models.CharField(max_length=100, blank=True, null=True)  # ✅ Matches `status`
    release_date = models.DateField(null=True, blank=True)  # ✅ Matches `release_date`
    poster_path = models.URLField(blank=True, null=True)  # ✅ Matches `poster_path`
    cast = models.JSONField(default=list)  # ✅ Corrected
    watch_platforms = models.JSONField(default=dict)  # ✅ Corrected
    content_type = models.CharField(
        max_length=50, choices=[("Movie", "Movie"), ("TV Series", "TV Series")]
    )  # ✅ Matches `content_type`
    popularity = models.FloatField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    runtime = models.CharField(max_length=50, blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)  # ✅ Store BERT embedding

    def save(self, *args, **kwargs):
        """Generate diverse embeddings using title, genres, cast, and platforms."""
        if not self.embedding:
            genre_keywords = {
                "โรแมนติก": "รัก หวาน คู่รัก จูบ ความสัมพันธ์ อบอุ่น แฟน ความรัก",
                "ตลก": "ตลก ขำขัน ฮาๆ สนุก คอมเมดี้ เบาสมอง ฮาไม่ไหว",
                "แอคชั่น": "แอคชั่น ต่อสู้ ยิง ระเบิด ตื่นเต้น ลุ้น",
                "ดราม่า": "เศร้า เสียน้ำตา เรื่องจริง ละครชีวิต",
                "สยองขวัญ": "ผี หลอน ฆาตกรรม น่ากลัว มืดมน",
            }

            # ✅ Add more weight to genres
            genre_text = " ".join(self.genres)
            for genre in self.genres:
                if genre in genre_keywords:
                    genre_text += " " + genre_keywords[genre]

            # ✅ Convert cast to text format
            cast_text = " ".join(
                [actor.split(" (")[0] for actor in self.cast]
            ) if isinstance(self.cast, list) else ""

            # ✅ Convert watch platforms to text
            platform_text = ", ".join(
                [f"{country}: {', '.join(data.get('streaming', ['N/A']))}"
                 for country, data in self.watch_platforms.items()]
            )

            # ✅ Generate unique text for embedding
            combined_text = f"{self.title_en} {self.title_th} {genre_text} {cast_text} {platform_text} {self.content_type} {self.status}"
            print(f"🔄 Generating embedding for: {self.title_en}")

            embedding_vector = get_bert_embedding(combined_text)
            self.embedding = json.dumps(embedding_vector)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title_th} ({self.title_en})"
