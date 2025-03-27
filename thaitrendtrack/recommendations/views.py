import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

import json
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from deep_translator import GoogleTranslator

from .forms import CustomUserCreationForm
from .models import Community, Post, Comment, Poll, Hashtag, Movie, Vote  # Combined all model imports
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from .models import UserProfile

# ✅ โหลดโมเดล
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model = AutoModel.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model.eval()

# ✅ โหลด embeddings
embedding_file = "movie_embeddings.pkl"
try:
    with open(embedding_file, "rb") as f:
        movie_embeddings = pickle.load(f)
    movie_embeddings = np.array(movie_embeddings).reshape(len(movie_embeddings), -1)
    print("✅ Loaded precomputed embeddings from file.")
except FileNotFoundError:
    print("❌ Error: Embeddings file not found. Please generate embeddings first.")
    movie_embeddings = None


# ✅ ฟังก์ชันแปลภาษาเป็นไทย
def translate_to_thai(text):
    return GoogleTranslator(source="auto", target="th").translate(text)


# ✅ ฟังก์ชันแปลงข้อความเป็น embedding
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze(0).numpy()


# ✅ ฟังก์ชันตรวจจับแนวหนัง
def detect_genre(description):
    genre_keywords = {
        "โรแมนติก": ["รัก", "โรแมนติก", "แฟน", "ความรัก", "อกหัก", "หวาน"],
        "สยองขวัญ": ["ผี", "สยองขวัญ", "น่ากลัว", "หลอน", "ฆาตกรรม", "วิญญาณ"],
        "แอคชั่น": ["บู๊", "แอคชั่น", "ต่อสู้", "ยิง", "ระเบิด"],
        "ตลก": ["ตลก", "ขำ", "ฮา", "สนุก"],
        "ดราม่า": ["ดราม่า", "ชีวิต", "เศร้า", "น้ำตา", "ซึ้ง"],
        "วิทยาศาสตร์": ["ไซไฟ", "วิทยาศาสตร์", "หุ่นยนต์", "อนาคต"],
        "แฟนตาซี": ["เวทมนตร์", "แฟนตาซี", "เทพนิยาย", "อัศวิน"],
        "อาชญากรรม": ["อาชญากรรม", "ตำรวจ", "นักสืบ", "สืบสวน"],
    }

    for genre, keywords in genre_keywords.items():
        if any(keyword in description.lower() for keyword in keywords):
            return genre

    return None  # ถ้าไม่พบแนวที่ชัดเจน


# ✅ Django View สำหรับค้นหาหนังที่คล้ายกับข้อความที่ป้อน
def definition_movies(request):
    query_text = request.GET.get("searchQuery", "").strip()

    if not query_text:
        return render(request, "definition_movies.html", {"movies": [], "search_query": query_text})

    print(f"🔎 Searching for: {query_text}")

    # ✅ แปลข้อความเป็นไทย
    query_text_thai = translate_to_thai(query_text)
    print(f"🔄 แปลงเป็นไทย: {query_text_thai}")

    # ✅ ตรวจจับแนวหนังจากคำบรรยาย
    detected_genre = detect_genre(query_text_thai)
    if detected_genre:
        print(f"🎭 แนวหนังที่พบ: **{detected_genre}**")

    # ✅ คำนวณ embedding ของข้อความค้นหา
    query_embedding = np.array(get_embedding(query_text_thai)).reshape(1, -1)

    # ✅ โหลดข้อมูลหนังจาก Database
    movies = Movie.objects.exclude(embedding__isnull=True)

    if not movies.exists():
        print("⚠️ ไม่มีหนังที่มี embeddings!")
        return render(request, "definition_movies.html", {"movies": [], "search_query": query_text})

    # ✅ โหลด embeddings จาก Movie Model
    movie_embeddings = []
    movie_list = []

    for movie in movies:
        if movie.embedding:
            emb = np.array(pickle.loads(movie.embedding)).reshape(1, -1)
            movie_embeddings.append(emb)
            movie_list.append(movie)

    movie_embeddings = np.vstack(movie_embeddings)
    print(f"✅ Movie Embeddings Shape: {movie_embeddings.shape}")

    # ✅ คำนวณ Cosine Similarity
    similarities = cosine_similarity(query_embedding, movie_embeddings).flatten()

    # ✅ Normalize similarity scores
    min_sim, max_sim = similarities.min(), similarities.max()
    similarities = (similarities - min_sim) / (max_sim - min_sim) if max_sim > min_sim else similarities

    print(f"✅ Normalized Similarities: {similarities}")

    # ✅ จัดเรียงผลลัพธ์ตาม similarity
    ranked_movies = sorted(zip(movie_list, similarities), key=lambda x: x[1], reverse=True)

    # ✅ กรองหนังที่ตรงแนวกับที่ค้นหา
    recommended_movies = []
    seen_movies = set()

    for m, sim in ranked_movies:
        if m.id not in seen_movies and sim > 0.3:
            recommended_movies.append({
                "id": m.id,
                "title_en": m.title_en,
                "title_th": m.title_th,
                "release_date": m.release_date.strftime("%Y") if m.release_date else "N/A",
                "poster_path": m.poster_path
            })
            seen_movies.add(m.id)

    if not recommended_movies:
        print("⚠️ ไม่พบหนังที่คล้ายกัน")
        return render(request, "definition_movies.html", {"movies": [], "search_query": query_text})

    return render(request, "definition_movies.html", {"movies": recommended_movies[:5], "search_query": query_text})


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies_detailed.html', {'movie': movie})


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


def movies_by_category(request, category):
    # Convert English category to Thai
    category_thai = GENRE_MAPPING.get(category, category)  # Default to input if not found
    print(f"🔍 Searching for movies in category: {category} ({category_thai})")  # Debugging

    # Check if genres are stored as JSON or strings
    try:
        movies = [movie for movie in Movie.objects.all() if category_thai in json.loads(movie.genres)]
    except TypeError:  # If genres are already lists
        movies = [movie for movie in Movie.objects.all() if category_thai in movie.genres]

    print(f"✅ Found {len(movies)} movies in category: {category} ({category_thai})")  # Debugging

    context = {
        "category": category,
        "movies": movies,
    }
    return render(request, "movies_category.html", context)


def settings_view(request):
    return render(request, 'settings.html')


# @csrf_exempt
# def recommend_movies_advanced(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#
#             # Your logic for filtering and recommending movies
#             recommended_movies = Movie.objects.all()[:5]
#
#             return JsonResponse({
#                 "success": True,
#                 "recommended_movies": [
#                     {
#                         'id': movie.id,
#                         'title_en': movie.title_en,
#                         'title_th': movie.title_th,
#                         'release_date': movie.release_date.strftime('%Y'),
#                         'poster_path': movie.poster_path,
#                     }
#                     for movie in recommended_movies
#                 ]
#             })
#
#         except Exception as e:
#             # Return an error if something goes wrong in the backend
#             return JsonResponse({"error": str(e)}, status=500)
#
#     return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)
# def load_embeddings():
#     try:
#         # Assuming the embeddings are stored in a file called 'movie_embeddings.pkl'
#         with open('recommendations\movie_embeddings.pkl', 'rb') as file:
#             embeddings = pickle.load(file)
#         return embeddings
#     except FileNotFoundError:
#         print("Embeddings file not found.")
#         return None
#     except Exception as e:
#         print(f"Error loading embeddings: {e}")
#         return None
#
#
# @csrf_exempt
# def recommend_movies_advanced(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#
#             # Filter the movies based on user input
#             genre = data.get('genre', "")
#             cast = data.get('cast', "")
#             description = data.get('description', "")
#             start_date = data.get('start_date', "")
#             end_date = data.get('end_date', "")
#
#             # Check if at least one filter is provided
#             if not any([genre, cast, description, start_date, end_date]):
#                 return JsonResponse({"error": "Please fill in at least one field."}, status=400)
#
#             # Predefined movie embeddings loaded previously
#             movie_embeddings = load_embeddings()
#
#             if movie_embeddings is None:
#                 raise Exception("Embeddings file not found")
#
#             # Apply filters
#             filtered_movies = Movie.objects.all()
#
#             if genre:
#                 filtered_movies = filtered_movies.filter(genres__icontains=genre)
#
#             if cast:
#                 filtered_movies = filtered_movies.filter(cast__icontains=cast)
#
#             if start_date and end_date:
#                 filtered_movies = filtered_movies.filter(release_date__range=[start_date, end_date])
#
#             # If description is provided, we use embeddings to find the most relevant movies
#             if description:
#                 user_embedding = get_embedding.py(description).reshape(1, -1)
#                 movie_embeddings_list = []
#
#                 for movie in filtered_movies:
#                     if movie.embedding:
#                         movie_embedding = pickle.loads(movie.embedding)  # Assuming precomputed embeddings
#                         movie_embeddings_list.append(movie_embedding)
#
#                 # Compute cosine similarity between the description and movie embeddings
#                 movie_embeddings_array = np.array(movie_embeddings_list)
#                 similarities = cosine_similarity(user_embedding, movie_embeddings_array).flatten()
#
#                 # Sort movies by similarity score
#                 filtered_movies = sorted(zip(filtered_movies, similarities), key=lambda x: x[1], reverse=True)
#                 filtered_movies = [movie for movie, _ in filtered_movies]
#
#             # Limit results to top 20 recommended movies
#             recommended_movies = filtered_movies[:20]
#
#             # Store the recommended movies in the session
#             request.session['recommended_movies'] = [
#                 {
#                     'id': movie.id,
#                     'title_en': movie.title_en,
#                     'title_th': movie.title_th,
#                     'release_date': movie.release_date.strftime('%Y') if movie.release_date else 'N/A',
#                     'poster_path': movie.poster_path,
#                 }
#                 for movie in recommended_movies
#             ]
#
#             return JsonResponse({
#                 "success": True,
#                 "recommended_movies": [
#                     {
#                         'id': movie.id,
#                         'title_en': movie.title_en,
#                         'title_th': movie.title_th,
#                         'release_date': movie.release_date.strftime('%Y') if movie.release_date else 'N/A',
#                         'poster_path': movie.poster_path,
#                     }
#                     for movie in recommended_movies
#                 ]
#             })
#
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#
#     return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)

# Load pre-trained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
model = AutoModel.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


def load_embeddings():
    embedding_file = os.path.join(settings.BASE_DIR, 'movie_embeddings.pkl')
    print(f"Loading embeddings from: {embedding_file}")  # Log the full path
    try:
        with open(embedding_file, "rb") as f:
            embeddings = pickle.load(f)

        # Check if embeddings are loaded correctly
        if not embeddings:
            print("❌ Error: Embeddings file is empty.")
        else:
            print(f"Loaded {len(embeddings)} movie embeddings.")

        return np.array(embeddings).reshape(len(embeddings), -1)
    except FileNotFoundError:
        print("❌ Error: Embeddings file not found. Please generate embeddings first.")
        return None


# Function to get text embeddings from description
def get_embedding_advanced(text):
    if not text.strip():  # Check if the description is empty or contains only spaces
        return np.array([])  # Return an empty array if the description is invalid

    prompt = f"ให้คำแนะนำหนังที่ตรงกับคำอธิบายต่อไปนี้: '{text}' โดยคำนึงถึงแนวหนัง เรื่องย่อ และความนิยม"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)

    # Ensure the embedding is 2D (1 sample with 768 features)
    embedding = outputs.last_hidden_state[:, 0, :].squeeze(0).numpy()

    # Ensure it's 2D for cosine similarity
    return embedding.reshape(1, -1)  # Reshape to ensure it's 2D


@csrf_exempt
def recommend_movies_advanced(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Get filters from the request body
            genre = data.get('genre', "")
            cast = data.get('cast', "")
            description = data.get('description', "")
            start_date = data.get('start_date', "")
            end_date = data.get('end_date', "")

            # Check if at least one filter is provided
            if not any([genre, cast, description, start_date, end_date]):
                return JsonResponse({"error": "Please fill in at least one field."}, status=400)

            # Load precomputed movie embeddings
            movie_embeddings = load_embeddings()

            if movie_embeddings is None:
                raise Exception("Embeddings file not found")

            # Apply filters to the Movie model
            filtered_movies = Movie.objects.all()

            if genre:
                filtered_movies = filtered_movies.filter(genres__icontains=genre)

            if cast:
                filtered_movies = filtered_movies.filter(cast__icontains=cast)

            if start_date and end_date:
                filtered_movies = filtered_movies.filter(release_date__range=[start_date, end_date])

            # If description is provided, use embeddings to find the most relevant movies
            if description:
                user_embedding = get_embedding_advanced(description)

                # Check if the user_embedding is empty
                if user_embedding.size == 0:  # If empty, return an error
                    return JsonResponse({"error": "Description is too short or empty for embedding."}, status=400)

                movie_embeddings_list = []

                for movie in filtered_movies:
                    if movie.embedding:
                        movie_embedding = pickle.loads(movie.embedding)  # Deserialize the stored embedding
                        movie_embeddings_list.append(movie_embedding)

                # Ensure the movie embeddings are reshaped correctly
                movie_embeddings_array = np.array(movie_embeddings_list)

                # Check if movie_embeddings_array is valid
                if movie_embeddings_array.size == 0:  # Check if movie embeddings are empty
                    return JsonResponse({"error": "No movie embeddings available."}, status=400)

                # Compute cosine similarity between user description and movie embeddings
                similarities = cosine_similarity(user_embedding, movie_embeddings_array).flatten()

                # Sort movies by similarity score in descending order
                filtered_movies = sorted(zip(filtered_movies, similarities), key=lambda x: x[1], reverse=True)
                filtered_movies = [movie for movie, _ in filtered_movies]

            # Limit results to top 20 recommended movies
            recommended_movies = filtered_movies[:20]

            # Prepare the response data for the recommended movies
            response_data = [
                {
                    'id': movie.id,
                    'title_en': movie.title_en,
                    'title_th': movie.title_th,
                    'release_date': movie.release_date.strftime('%Y') if movie.release_date else 'N/A',
                    'poster_path': movie.poster_path,
                }
                for movie in recommended_movies
            ]

            # Return the response as a JSON object
            return JsonResponse({
                "success": True,
                "recommended_movies": response_data
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)


def movies_advance(request):
    # Fetch recommended movies from the session (if any)
    recommended_movies = request.session.get('recommended_movies', [])

    # If no movies in the session, you can fetch all movies or any specific category
    if not recommended_movies:
        recommended_movies = Movie.objects.all()

    # Pass the movies to the template
    return render(request, 'movies_advance.html', {'movies': recommended_movies})


@login_required
def homepage(request):
    movies = Movie.objects.filter(content_type="Movie")[:10]
    series = Movie.objects.filter(content_type="TV Series")[:10]

    print("Movies in context:", movies.count())
    print("Series in context:", series.count())  # ✅ Debug

    return render(request, 'homepage.html', {
        'movies': movies,
        'series': series
    })


ALL_GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"
]


@login_required
def settings_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        new_preferences = request.POST.getlist("preferences")  # Get updated preferences
        user_profile.preferences = new_preferences  # Save new preferences
        user_profile.save()
        return redirect("settings")  # Refresh page after saving

    context = {
        "username": request.user.username,
        "email": request.user.email,
        "preferences": user_profile.preferences,  # Previously selected preferences
        "available_genres": ALL_GENRES,  # All possible genres
    }
    return render(request, "settings.html", context)


@login_required
def save_preferences(request):
    if request.method == "POST":
        selected_preferences = request.POST.getlist("genres[]")  # Get selected genres
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.preferences = selected_preferences
        user_profile.save()
        return JsonResponse({"success": True})  # ✅ Return JSON success response

    return render(request, "edit_preferences.html")


def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Redirect back to settings page

    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})


@login_required
def community_home(request):
    selected_club = request.GET.get('club')  # Get the selected club ID from the request
    communities = Community.objects.all()  # Get all communities
    if selected_club:
        # Filter posts by selected club
        community = get_object_or_404(Community, id=selected_club)
        posts = Post.objects.filter(community=community).order_by('-created_at')
    else:
        # If no club is selected, show all posts
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'communities.html', {'communities': communities, 'posts': posts})


@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(community=community, user=request.user, content=content)
        return redirect('community_home', community_id=community.id)


@login_required
def settings_view(request):
    user_profile = request.user.userprofile  # Access the user profile information
    return render(request, 'settings.html', {'user_profile': user_profile})


@login_required
def update_profile(request):
    user_profile = request.user.userprofile  # Get the logged-in user's profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Redirect back to the settings page
    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'update_profile.html', {'form': form})


# @login_required
# def community_home(request):
#     selected_club = request.GET.get('club')
#     communities = Community.objects.all()
#     posts = Post.objects.all().order_by('-created_at')
#
#     if selected_club:
#         community = get_object_or_404(Community, name=selected_club)
#         posts = Post.objects.filter(community=community).order_by('-created_at')
#
#     if request.method == 'POST':
#         # Handle comment submission
#         if 'comment' in request.POST:
#             post_id = request.POST.get('post_id')
#             comment_content = request.POST.get('comment')
#             post = get_object_or_404(Post, id=post_id)
#             Comment.objects.create(post=post, user=request.user, content=comment_content)
#             return redirect('community_home')
#
#         # Handle new post creation with poll and hashtags
#         content = request.POST.get('content')
#         image = request.FILES.get('image')
#         community_id = request.POST.get('community_id')
#         community = get_object_or_404(Community, id=community_id)
#
#         # Handle Hashtag Creation
#         hashtags_input = request.POST.get('hashtags')  # Get the hashtags input as a comma-separated string
#         hashtags = [Hashtag.objects.get_or_create(name=tag.strip())[0] for tag in
#                     hashtags_input.split(',')]  # Create or get existing hashtags
#
#         # Create the post
#         new_post = Post.objects.create(
#             community=community,
#             user=request.user,
#             content=content,
#             image=image
#         )
#
#         # Assign hashtags to the post
#         new_post.hashtags.set(hashtags)
#         new_post.save()
#
#         # Handle Poll Creation
#         poll_question = request.POST.get('poll_question')
#         poll_choices = request.POST.getlist('poll_choices')
#         for key in request.POST:
#             if key.startswith("poll_choice_"):
#                 poll_choices.append(request.POST[key])
#         if poll_question and poll_choices:
#             poll = Poll.objects.create(
#                 question=poll_question,
#                 choices=poll_choices  # Store choices as a list
#             )
#         new_post.poll = poll
#         new_post.save()
#
#         # Display poll choices and their counts
#         for post in posts:
#             if post.poll:
#                 # Get the choices from the poll and count the votes for each
#                 post.poll.vote_counts = {
#                     choice: post.poll.votes.filter(choice=choice).count()
#                     for choice in post.poll.choices
#                 }
#
#         return redirect('community_home')
#
#     # Calculate vote counts for each post with polls
#     for post in posts:
#         if post.poll:
#             post.poll.vote_counts = {
#                 choice: post.poll.votes.filter(choice=choice).count()
#                 for choice in post.poll.choices
#             }
#
#     return render(request, 'communities.html', {
#         'communities': communities,
#         'posts': posts,
#         'selected_club': selected_club,
#     })

@login_required
def community_home(request):
    selected_club = request.GET.get('club')
    communities = Community.objects.all()
    posts = Post.objects.all().order_by('-created_at')

    # Filter posts by selected club
    if selected_club:
        community = get_object_or_404(Community, name=selected_club)
        posts = Post.objects.filter(community=community).order_by('-created_at')

    if request.method == 'POST':
        # Handle comment submission
        if 'comment' in request.POST:
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment')
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, user=request.user, content=comment_content)
            return redirect('community_home')

        # Handle new post creation with poll and hashtags
        content = request.POST.get('content')
        image = request.FILES.get('image')
        community_id = request.POST.get('community_id')
        community = get_object_or_404(Community, id=community_id)

        # Handle Hashtag Creation
        hashtags_input = request.POST.get('hashtags')  # Get the hashtags input as a comma-separated string
        hashtags = [Hashtag.objects.get_or_create(name=tag.strip())[0] for tag in
                    hashtags_input.split(',')]  # Create or get existing hashtags

        # Create the post
        new_post = Post.objects.create(
            community=community,
            user=request.user,
            content=content,
            image=image
        )

        # Assign hashtags to the post
        new_post.hashtags.set(hashtags)
        new_post.save()

        # Handle Poll Creation
        poll_question = request.POST.get('poll_question')
        poll_choices_raw = request.POST.get('poll_choices')  # รับค่าเป็นสตริง
        poll_choices = [choice.strip() for choice in poll_choices_raw.split(',') if choice.strip()]
        for key in request.POST:
            if key.startswith("poll_choice_"):
                poll_choices.append(request.POST[key])

        # If poll question and choices are provided, create a new poll
        if poll_question and poll_choices:
            poll = Poll.objects.create(
                question=poll_question,
                choices=poll_choices  # Store choices as a list
            )
            new_post.poll = poll
            new_post.save()

        return redirect('community_home')

    # Calculate vote counts and percentages for each post with polls
    for post in posts:
        if post.poll:
            vote_counts = {choice: post.poll.votes.filter(choice=choice).count() for choice in post.poll.choices}
            total_votes = sum(vote_counts.values())

            # Calculate vote percentages
            vote_percentages = {choice: (count / total_votes * 100 if total_votes > 0 else 0) for choice, count in
                                vote_counts.items()}

            # Find the leading choice and its percentage
            leading_choice = max(vote_percentages, key=vote_percentages.get, default=None)
            leading_percent = vote_percentages.get(leading_choice, 0)

            # Add vote counts and percentages to the post
            post.poll.vote_counts = vote_counts
            post.poll.vote_percentages = vote_percentages
            post.poll.leading_choice = leading_choice
            post.poll.leading_percent = leading_percent

    return render(request, 'communities.html', {
        'communities': communities,
        'posts': posts,
        'selected_club': selected_club,
    })


@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(community=community, user=request.user, content=content, image=image)
        return redirect('community_home')

    return render(request, 'create_post.html', {'community': community})


@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('community_home')


@login_required
def hashtag_posts(request, hashtag_name):
    # Retrieve the hashtag object from the database
    hashtag = Hashtag.objects.get(name=hashtag_name)

    # Retrieve posts that contain the given hashtag
    posts = Post.objects.filter(hashtags=hashtag).order_by('-created_at')

    # Return the posts to the template
    return render(request, 'communities.html', {
        'posts': posts,
        'selected_club': 'all',  # If you have a selected club, you can modify this
        'hashtag': hashtag_name
    })


@login_required
def like_post(request, post_id):
    if request.method == "POST":
        try:
            post = get_object_or_404(Post, id=post_id)

            # Check if the user has already liked the post
            if post.likes.filter(id=request.user.id).exists():
                # If liked, unlike by removing the user from the likes
                post.likes.remove(request.user)
                is_liked = False
            else:
                # If not liked, add the user to the likes
                post.likes.add(request.user)
                is_liked = True

            post.save()

            # Return the updated like count and like status (liked or unliked)
            return JsonResponse({'likes_count': post.likes.count(), 'is_liked': is_liked}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Delete Comment View

def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)

        # Ensure the user is the author of the comment
        if comment.user == request.user:
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'}, status=200)

        return JsonResponse({'error': 'You can only delete your own comments'}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# View to delete post
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        # Ensure that the user is the owner of the post
        if post.user == request.user:
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'You can only delete your own posts'}, status=403)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)  # หา Poll ตาม id

    if request.method == "POST":
        choice = request.POST.get('choice')  # รับข้อมูลตัวเลือกที่ผู้ใช้เลือก

        if choice:
            # สร้างการโหวตใหม่
            Vote.objects.create(
                user=request.user,  # ผู้ใช้ที่ทำการโหวต
                poll=poll,  # Poll ที่ทำการโหวต
                choice=choice  # ตัวเลือกที่เลือก
            )

            # ส่งผู้ใช้กลับไปยังหน้าโพสต์หรือที่อื่นๆ
            return redirect('poll_results', poll_id=poll.id)
    else:
        # ถ้าไม่ได้ใช้ POST ให้แสดงผลลัพธ์
        return render(request, 'vote.html', {'poll': poll})


def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    votes = Vote.objects.filter(poll=poll)

    # สรุปผลการโหวต
    results = {choice: votes.filter(choice=choice).count() for choice in poll.get_choices}

    return render(request, 'poll_results.html', {'poll': poll, 'results': results})


# @csrf_exempt
# def vote(request, post_id):
#     post = get_object_or_404(Post, id=post_id)  # Retrieve the post based on the post_id
#     if request.method == 'POST':
#         poll_choice = request.POST.get('poll_choice')  # Get the poll choice from the form
#         if poll_choice:
#             # Save the vote in the database
#             Vote.objects.create(post=post, user=request.user, choice=poll_choice)
#             return redirect('community_home')  # Redirect after voting
#     return redirect('community_home')  # Redirect if method is not POST or no choice is selected

@csrf_exempt
def vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    poll_choice = request.POST.get('poll_choice')  # Ensure you have the poll choice from the form

    if poll_choice is None:
        print("Poll choice was not passed correctly")
        return redirect('community_home')  # Handle this case more gracefully, maybe with an error message

    # Create a vote for the poll choice
    vote = Vote.objects.create(
        post=post,
        user=request.user,
        choice=poll_choice
    )

    return redirect('community_home')  # Or wherever you want to redirect

@login_required
def vote_poll(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    poll = post.poll

    if request.method == 'POST':
        choice = request.POST.get('poll_choice')
        if choice is not None:
            # Create a new vote for the selected choice
            Vote.objects.create(
                user=request.user,
                poll=poll,
                choice=poll.choices[int(choice)]
            )

            # Update vote counts and percentages
            poll.vote_counts = {choice: poll.votes.filter(choice=choice).count() for choice in poll.choices}
            total_votes = sum(poll.vote_counts.values())

            poll.vote_percentages = {
                choice: (count / total_votes * 100 if total_votes > 0 else 0) for choice, count in poll.vote_counts.items()
            }
            poll.leading_choice = max(poll.vote_percentages, key=poll.vote_percentages.get)
            poll.leading_percent = poll.vote_percentages[poll.leading_choice]
            poll.save()

            return redirect('community_home')  # Redirect to the community home page

    return redirect('community_home')  # If not POST, redirect back to home
