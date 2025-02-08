# import pickle
# import numpy as np
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from sklearn.metrics.pairwise import cosine_similarity
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import login as auth_login
# from .models import UserProfile
# from .forms import CustomUserCreationForm
# from django.shortcuts import render, get_object_or_404
# from .models import Movie
# from transformers import AutoTokenizer, AutoModel
# import torch
# from sklearn.metrics.pairwise import cosine_similarity
#
# # โหลด Tokenizer และ Model
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# model = AutoModel.from_pretrained("bert-base-uncased")
#
#
# def movies(request):
#     # Fetch all movies from the database
#     all_movies = Movie.objects.all()
#
#     # Return a template with all movies (or return them in a JSON response)
#     return render(request, 'movies_list.html', {'movies': all_movies})
#
# def movie_list(request):
#     movies = Movie.objects.all()
#     return render(request, 'movies.html', {'movies': movies})
#
#
# def movie_detail(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     return render(request, 'movies_detailed.html', {'movie': movie})
#
#
# # ฟังก์ชันสำหรับแปลงข้อความเป็นเวกเตอร์
# def get_embeddings(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)
#
#
# # Genre mapping dictionary
# GENRE_MAPPING = {
#     "Action": "บู๊",
#     "Adventure": "ผจญ",
#     "Crime": "อาชญากรรม",
#     "Drama": "หนังชีวิต",
#     "Thriller": "ระทึกขวัญ",
#     "Horror": "สยองขวัญ",
#     "Animation": "แอนนิเมชั่น",
#     "Fantasy": "จินตนาการ",
#     "Romance": "หนังรักโรแมนติก",
#     "Science Fiction": "นิยายวิทยาศาสตร์",
#     "Documentary": "สารคดี",
#     "Comedy": "ตลก",
#     "Western": "หนังคาวบอยตะวันตก",
#     "Mystery": "ลึกลับ",
#     "War": "สงคราม",
#     "History": "ประวัติศาสตร์",
#     "Music": "ดนตรี",
#     "Family": "ครอบครัว",
#     "TV Movie": "ภาพยนตร์โทรทัศน์"
# }
#
#
# # Sign Up Function
# # def signup(request):
# #     if request.method == 'POST':
# #         form = CustomUserCreationForm(request.POST)  # ใช้ CustomUserCreationForm
# #         if form.is_valid():
# #             user = form.save()
# #             auth_login(request, user)  # Login after signup
# #             return redirect('preferences')  # Redirect to preferences page
# #     else:
# #         form = CustomUserCreationForm()  # ใช้ CustomUserCreationForm
# #     return render(request, 'signup.html', {'form': form})
# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)  # Use CustomUserCreationForm
#         if form.is_valid():
#             user = form.save()
#             # auth_login(request, user)  # Login after signup
#
#             # Explicitly create the UserProfile after user creation
#             UserProfile.objects.get_or_create(user=user)
#
#             return redirect('preferences')  # Redirect to preferences page
#     else:
#         form = CustomUserCreationForm()  # Use CustomUserCreationForm
#     return render(request, 'signup.html', {'form': form})
#
#
# # Login Function
# def custom_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#
#             # Check if first login
#             user_profile, created = UserProfile.objects.get_or_create(user=user)
#             if user_profile.is_first_login:
#                 user_profile.is_first_login = False
#                 user_profile.save()
#                 return redirect('preferences')
#             return redirect('homepage')  # Redirect to homepage on subsequent logins
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})
#
#
# # Preferences Function
# # @login_required
# # def preferences(request):
# #     if request.method == "POST":
# #         selected_preferences = request.POST.getlist('genres[]')
# #         request.session['preferences'] = selected_preferences
# #         user_profile = UserProfile.objects.get(user=request.user)
# #         user_profile.preferences = selected_preferences
# #         user_profile.save()
# #         return redirect('recommend')
# #     return render(request, 'preference.html')
# @login_required
# def preferences(request):
#     if request.method == "POST":
#         # Retrieve selected preferences from the form
#         selected_preferences = request.POST.getlist('genres[]')
#
#         # Debug: Log the received preferences
#         print(f"Selected Preferences: {selected_preferences}")
#
#         # Save preferences to the session
#         request.session['preferences'] = selected_preferences
#
#         # Save preferences to the UserProfile
#         try:
#             user_profile = UserProfile.objects.get(user=request.user)
#             user_profile.preferences = selected_preferences
#             user_profile.save()
#
#             # Debug: Confirm saving in the database
#             print(f"Preferences saved: {user_profile.preferences}")
#
#         except UserProfile.DoesNotExist:
#             print("UserProfile not found for the user!")
#
#         return redirect('recommend')
#
#     return render(request, 'preference.html')
#
#
# # @csrf_exempt
# # def recommend(request):
# #     if request.method == "POST":
# #         # Retrieve the selected genres from POST data
# #         selected_genres = request.POST.getlist('genres[]')
# #         selected_genres_ids = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]
# #
# #         # Load movie data from the CSV file
# #         csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"  # Adjust to the actual path
# #         try:
# #             movies_df = pd.read_csv(csv_path)
# #
# #             # Handle missing or NaN values in 'genres'
# #             movies_df['genres'] = movies_df['genres'].fillna('').astype(str)
# #
# #             # Filter movies that match the selected genres
# #             def genre_filter(genres):
# #                 genre_list = genres.split(', ')
# #                 return any(genre in genre_list for genre in selected_genres_ids)
# #
# #             filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]
# #
# #             # Sort movies by popularity, vote_average, and release_date
# #             sorted_movies = filtered_movies.sort_values(
# #                 by=['popularity', 'vote_average', 'release_date'],
# #                 ascending=[False, False, False]
# #             )
# #
# #             # Limit to the top 10 recommended movies
# #             recommended_movies = sorted_movies.head(10).to_dict(orient='records')
# #
# #             # Include poster URLs and titles
# #             for movie in recommended_movies:
# #                 movie['poster_path'] = movie.get('poster_path', 'No poster available')
# #                 movie['title_en'] = movie.get('title_en', 'No English title available')
# #                 movie['title_th'] = movie.get('title_th', 'No Thai title available')
# #
# #             # Render the movies.html page with the recommendations
# #             return render(request, 'movies.html', {
# #                 'movies': recommended_movies,
# #                 'selected_genres': selected_genres,
# #                 'selected_genres_ids': selected_genres_ids
# #             })
# #         except FileNotFoundError:
# #             return render(request, 'movies.html', {
# #                 'error_message': "The movie dataset file was not found. Please check the file path."
# #             })
# #         except Exception as e:
# #             return render(request, 'movies.html', {
# #                 'error_message': f"An error occurred: {str(e)}"
# #             })
# #
# #     # If it's a GET request or invalid method, redirect to preferences
# #     return redirect('preferences')
#
# @csrf_exempt
# def recommend(request):
#     if request.method == "POST":
#         selected_genres = request.POST.getlist('genres[]')
#
#         # ใช้ฐานข้อมูล Movie แทน CSV
#         recommended_movies = Movie.objects.filter(genres__overlap=selected_genres).order_by('-release_date')[:10]
#
#         # Debugging
#         print(f"🔥 พบหนัง {recommended_movies.count()} เรื่อง")
#         for movie in recommended_movies:
#             print(f"🎬 {movie.id}: {movie.title_en}")
#
#         return render(request, 'movies.html', {
#             'movies': recommended_movies,
#             'selected_genres': selected_genres
#         })
#
#     return redirect('preferences')
#
#
#
#
# # Homepage Function
# @login_required
# def homepage(request):
#     return render(request, 'homepage.html')
#
from datetime import date

import pandas as pd
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import UserProfile, Movie
from .forms import CustomUserCreationForm
from transformers import AutoTokenizer, AutoModel
from django.db.models import Q
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load Tokenizer and Model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")


def movies(request):
    # Fetch all movies from the database
    all_movies = Movie.objects.all()

    # Return a template with all movies
    return render(request, 'movies_list.html', {'movies': all_movies})


def movie_list(request):
    # Fetch all movies from the database
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})


def movie_detail(request, movie_id):
    # Fetch movie details by ID
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies_detailed.html', {'movie': movie})


# Function to convert text to embeddings
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)


# # Genre mapping dictionary
# GENRE_MAPPING = {
#     "Action": "บู๊",
#     "Adventure": "ผจญ",
#     "Crime": "อาชญากรรม",
#     "Drama": "หนังชีวิต",
#     "Thriller": "ระทึกขวัญ",
#     "Horror": "สยองขวัญ",
#     "Animation": "แอนนิเมชั่น",
#     "Fantasy": "จินตนาการ",
#     "Romance": "หนังรักโรแมนติก",
#     "Science Fiction": "นิยายวิทยาศาสตร์",
#     "Documentary": "สารคดี",
#     "Comedy": "ตลก",
#     "Western": "หนังคาวบอยตะวันตก",
#     "Mystery": "ลึกลับ",
#     "War": "สงคราม",
#     "History": "ประวัติศาสตร์",
#     "Music": "ดนตรี",
#     "Family": "ครอบครัว",
#     "TV Movie": "ภาพยนตร์โทรทัศน์"
# }
GENRE_MAPPING = {
    "Action": "บู๊",
    "Crime": "อาชญากรรม",
    "Drama": "หนังชีวิต",
    "Thriller": "ระทึกขวัญ",
    "Adventure": "ผจญ",
    "Fantasy": "จินตนาการ",
    "Comedy": "ตลก",
    "Horror": "สยองขวัญ",
    "Romance": "หนังรักโรแมนติก",
    "Western": "หนังคาวบอยตะวันตก",
    "Sci-Fi": "นิยายวิทยาศาสตร์",
    "Mystery": "ลึกลับ",
    "War": "สงคราม",
    "Family": "ครอบครัว",
    "Music": "ดนตรี",
    "History": "ประวัติศาสตร์",
    "Documentary": "สารคดี",
    "TV Movie": "ภาพยนตร์โทรทัศน์",
}


# Sign Up Function
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Explicitly create the UserProfile after user creation
            UserProfile.objects.get_or_create(user=user)

            return redirect('preferences')  # Redirect to preferences page
    else:
        form = CustomUserCreationForm()
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
        # Retrieve selected preferences from the form
        selected_preferences = request.POST.getlist('genres[]')

        # Debug: Log the received preferences
        print(f"Selected Preferences: {selected_preferences}")

        # Save preferences to the session
        request.session['preferences'] = selected_preferences

        # Save preferences to the UserProfile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.preferences = selected_preferences
            user_profile.save()

            # Debug: Confirm saving in the database
            print(f"Preferences saved: {user_profile.preferences}")

        except UserProfile.DoesNotExist:
            print("UserProfile not found for the user!")

        return redirect('recommend')

    return render(request, 'preference.html')


# @csrf_exempt
# def recommend(request):
#     if request.method == "POST":
#         # Retrieve the selected genres from POST data
#         selected_genres = request.POST.getlist('genres[]')
#         selected_genres_ids = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]
#
#         # Load movie data from the CSV file
#         csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"  # Adjust to the actual path
#         try:
#             movies_df = pd.read_csv(csv_path)
#
#             # Handle missing or NaN values in 'genres'
#             movies_df['genres'] = movies_df['genres'].fillna('').astype(str)
#
#             # Filter movies that match the selected genres
#             def genre_filter(genres):
#                 genre_list = genres.split(', ')
#                 return any(genre in genre_list for genre in selected_genres_ids)
#
#             filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]
#
#             # Sort movies by popularity, vote_average, and release_date
#             sorted_movies = filtered_movies.sort_values(
#                 by=['popularity', 'vote_average', 'release_date'],
#                 ascending=[False, False, False]
#             )
#
#             # Limit to the top 10 recommended movies
#             recommended_movies = sorted_movies.head(10).to_dict(orient='records')
#
#             # Include poster URLs and titles
#             for movie in recommended_movies:
#                 movie['poster_path'] = movie.get('poster_path', 'No poster available')
#                 movie['title_en'] = movie.get('title_en', 'No English title available')
#                 movie['title_th'] = movie.get('title_th', 'No Thai title available')
#
#             # Render the movies.html page with the recommendations
#             return render(request, 'movies.html', {
#                 'movies': recommended_movies,
#                 'selected_genres': selected_genres,
#                 'selected_genres_ids': selected_genres_ids
#             })
#         except FileNotFoundError:
#             return render(request, 'movies.html', {
#                 'error_message': "The movie dataset file was not found. Please check the file path."
#             })
#         except Exception as e:
#             return render(request, 'movies.html', {
#                 'error_message': f"An error occurred: {str(e)}"
#             })
#
#     # If it's a GET request or invalid method, redirect to preferences
#     return redirect('preferences')

from datetime import datetime


# @csrf_exempt
def recommend(request):
    if request.method == "POST":
        print("Received POST request.")

        # Retrieve the selected genres from POST data
        selected_genres = request.POST.getlist('genres[]')
        if not selected_genres:
            print("No genres selected.")
            return redirect('preferences')

        print(f"Selected genres (English): {selected_genres}")

        # Convert English genres to Thai using GENRE_MAPPING
        selected_genres_translated = [
            GENRE_MAPPING.get(genre, genre) for genre in selected_genres
        ]
        print(f"Translated genres (Thai): {selected_genres_translated}")

        # Retrieve all movies and filter them manually by genres
        all_movies = Movie.objects.all()
        filtered_movies = []

        # Check each movie's genres and log all genre data
        for movie in all_movies:
            print(f"Movie: {movie.title_en}, Genres: {movie.genres}")  # Debugging line

            # Ensure movie genres are stored as strings, split if necessary
            movie_genres = movie.genres  # Assuming `movie.genres` is a list of genre names as strings

            # Check that genres are stored as a list of full strings
            if isinstance(movie_genres, str):
                movie_genres = [genre.strip() for genre in movie_genres.split(',')]  # Split genres by comma if needed

            for genre in movie_genres:
                print(f"Comparing full genre '{genre}' with selected genres...")
                if genre in selected_genres_translated:
                    print(f"Match found! Movie {movie.title_en} contains genre '{genre}'")
                    filtered_movies.append(movie)
                    break  # Break once we find a match for efficiency

        print(f"Found {len(filtered_movies)} movies matching the selected genres.")

        if not filtered_movies:
            print("No movies found for the selected genres. Please check genre data.")

        # Sort filtered movies by popularity, vote_average, and release_date (descending)
        filtered_movies.sort(key=lambda x: (
            -x.popularity if x.popularity else 0,
            -x.vote_average if x.vote_average else 0,
            # Convert date to datetime for sorting by release date
            datetime.combine(x.release_date, datetime.min.time()) if x.release_date else datetime.min
        ))

        # Limit to the top 10 recommended movies
        recommended_movies = filtered_movies[:10]

        print(f"Top 10 recommended movies: {[movie.title_en for movie in recommended_movies]}")

        return render(request, 'movies.html', {
            'movies': recommended_movies,
            'selected_genres': selected_genres,
        })

    print("Redirecting to preferences.")
    return redirect('preferences')


# Homepage Function
@login_required
def homepage(request):
    return render(request, 'homepage.html')
