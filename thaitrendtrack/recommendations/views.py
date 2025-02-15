import numpy as np
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import UserProfile, Movie
from .forms import CustomUserCreationForm
from transformers import AutoTokenizer, AutoModel
from datetime import datetime
from django.db.models import Q
import torch
from sklearn.metrics.pairwise import cosine_similarity

from django.http import JsonResponse

# Load Tokenizer and Model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")


# def movie_detail(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     data = {
#         "english_title": movie.title_en,  # Ensure your field names match
#         "thai_title": movie.title_th,
#         "release_date": movie.release_date.strftime("%Y"),
#         "description": movie.description,
#     }
#     return JsonResponse(data)


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies_detailed.html', {'movie': movie})


# Function to convert text to embeddings
# def get_embeddings(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)


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
        # print(f"Selected Preferences: {selected_preferences}")

        # Save preferences to the session
        request.session['preferences'] = selected_preferences

        # Save preferences to the UserProfile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.preferences = selected_preferences
            user_profile.save()

            # Debug: Confirm saving in the database
            # print(f"Preferences saved: {user_profile.preferences}")

        except UserProfile.DoesNotExist:
            print("UserProfile not found for the user!")

        return redirect('recommend')

    return render(request, 'preference.html')


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


# Function to generate text embeddings
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


# Function to handle movie search
def search_movies(request):
    if request.method == "GET":
        query = request.GET.get("searchQuery", "").strip()
        if not query:
            return render(request, "movies.html", {"movies": []})

        user_embedding = get_embeddings(query)

        # Fetch all movies from the database
        movies = Movie.objects.all()

        # Compute similarity scores
        movie_data = []
        for movie in movies:
            movie_embedding = get_embeddings(movie.description) if movie.description else np.zeros((1, 768))
            similarity_score = cosine_similarity(user_embedding, movie_embedding).flatten()[0]
            movie_data.append((movie, similarity_score))

        # Sort movies by similarity score
        movie_data.sort(key=lambda x: x[1], reverse=True)
        recommended_movies = [
            {"title_en": m.title_en, "title_th": m.title_th, "similarity": s, "description": m.description} for m, s in
            movie_data[:10]]

        return render(request, "movies.html", {"movies": recommended_movies})


def recommend_movies(request):
    if request.method == "GET":
        query = request.GET.get("searchQuery", "").strip()
        if not query:
            return render(request, "recommend.html", {"movies": []})  # Redirect to recommend.html

        user_embedding = get_embeddings(query)

        # Fetch all movies
        movies = Movie.objects.all()

        # Compute similarity scores
        movie_data = []
        for movie in movies:
            if movie.description:
                movie_embedding = get_embeddings(movie.description)
            else:
                movie_embedding = np.zeros((1, user_embedding.shape[1]))  # Ensure correct shape

            similarity_score = cosine_similarity(user_embedding, movie_embedding).flatten()[0]
            movie_data.append((movie, similarity_score))

        # Sort movies by similarity
        movie_data.sort(key=lambda x: x[1], reverse=True)
        recommended_movies = [
            {
                "title_en": m.title_en,
                "title_th": m.title_th,
                "similarity": round(s, 3),
                "description": m.description
            }
            for m, s in movie_data[:10]
        ]

        return render(request, "recommend.html", {"movies": recommended_movies})  # Use recommend.html


# Homepage Function
@login_required
def homepage(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]  # ดึงมาแค่ 10 เรื่อง
    return render(request, 'homepage.html', {'movies': movies})
