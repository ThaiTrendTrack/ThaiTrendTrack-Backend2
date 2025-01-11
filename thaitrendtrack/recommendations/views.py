import pickle
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import UserProfile
from .forms import CustomUserCreationForm

from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# โหลด Tokenizer และ Model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")


# ฟังก์ชันสำหรับแปลงข้อความเป็นเวกเตอร์
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)


# Genre mapping dictionary
GENRE_MAPPING = {
    "Action": "บู๊",
    "Adventure": "ผจญ",
    "Crime": "อาชญากรรม",
    "Drama": "หนังชีวิต",
    "Thriller": "ระทึกขวัญ",
    "Horror": "สยองขวัญ",
    "Animation": "แอนนิเมชั่น",
    "Fantasy": "จินตนาการ",
    "Romance": "หนังรักโรแมนติก",
    "Science Fiction": "นิยายวิทยาศาสตร์",
    "Documentary": "สารคดี",
    "Comedy": "ตลก",
    "Western": "หนังคาวบอยตะวันตก",
    "Mystery": "ลึกลับ",
    "War": "สงคราม",
    "History": "ประวัติศาสตร์",
    "Music": "ดนตรี",
    "Family": "ครอบครัว",
    "TV Movie": "ภาพยนตร์โทรทัศน์"
}


# Sign Up Function
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # ใช้ CustomUserCreationForm
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Login after signup
            return redirect('preferences')  # Redirect to preferences page
    else:
        form = CustomUserCreationForm()  # ใช้ CustomUserCreationForm
    return render(request, 'signup.html', {'form': form})


# Login Function
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Check if first login
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if user_profile.is_first_login:
                user_profile.is_first_login = False
                user_profile.save()
                return redirect('preferences')
            return redirect('homepage')  # Redirect to homepage on subsequent logins
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Preferences Function
@login_required
def preferences(request):
    if request.method == "POST":
        selected_preferences = request.POST.getlist('genres[]')
        request.session['preferences'] = selected_preferences
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.preferences = selected_preferences
        user_profile.save()
        return redirect('recommend')
    return render(request, 'preference.html')


@csrf_exempt
def recommend(request):
    if request.method == "POST":
        # Retrieve the selected genres from POST data
        selected_genres = request.POST.getlist('genres[]')
        selected_genres_ids = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]

        # Load movie data from the CSV file
        csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"  # Adjust to the actual path
        try:
            movies_df = pd.read_csv(csv_path)

            # Handle missing or NaN values in 'genres'
            movies_df['genres'] = movies_df['genres'].fillna('').astype(str)

            # Filter movies that match the selected genres
            def genre_filter(genres):
                genre_list = genres.split(', ')
                return any(genre in genre_list for genre in selected_genres_ids)

            filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]

            # Sort movies by popularity, vote_average, and release_date
            sorted_movies = filtered_movies.sort_values(
                by=['popularity', 'vote_average', 'release_date'],
                ascending=[False, False, False]
            )

            # Limit to the top 10 recommended movies
            recommended_movies = sorted_movies.head(10).to_dict(orient='records')

            # Include poster URLs and titles
            for movie in recommended_movies:
                movie['poster_path'] = movie.get('poster_path', 'No poster available')
                movie['title_en'] = movie.get('title_en', 'No English title available')
                movie['title_th'] = movie.get('title_th', 'No Thai title available')

            # Render the movies.html page with the recommendations
            return render(request, 'movies.html', {
                'movies': recommended_movies,
                'selected_genres': selected_genres,
                'selected_genres_ids': selected_genres_ids
            })
        except FileNotFoundError:
            return render(request, 'movies.html', {
                'error_message': "The movie dataset file was not found. Please check the file path."
            })
        except Exception as e:
            return render(request, 'movies.html', {
                'error_message': f"An error occurred: {str(e)}"
            })

    # If it's a GET request or invalid method, redirect to preferences
    return redirect('preferences')


# Homepage Function
@login_required
def homepage(request):
    return render(request, 'homepage.html')