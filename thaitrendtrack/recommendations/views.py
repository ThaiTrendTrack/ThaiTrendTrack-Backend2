import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def preferences(request):
    if request.method == "POST":
        # Extract selected preferences from POST data
        selected_preferences = request.POST.getlist('preferences')

        # Save or process preferences
        request.session['preferences'] = selected_preferences

        # Redirect to recommendations
        return redirect('recommendations')

    return render(request, 'preference.html')


import pandas as pd
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def recommend(request):
    if request.method == "POST":
        # Get the user-selected genres
        selected_genres = request.POST.getlist('genres[]')
        selected_genres_thai = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]

        # Load the movie dataset
        csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Adjust the path as necessary
        movies_df = pd.read_csv(csv_path)

        # Ensure the 'genres' column is treated as a string and handle NaN values
        movies_df['genres'] = movies_df['genres'].fillna('').astype(str)

        # Filter movies based on selected genres
        def genre_filter(genres):
            return any(genre in genres for genre in selected_genres_thai)

        filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]

        # Sort movies by popularity, vote_average, and release_date
        sorted_movies = filtered_movies.sort_values(
            by=['popularity', 'vote_average', 'release_date'],
            ascending=[False, False, False]
        )

        # Prepare movie data for the recommendation page
        recommended_movies = sorted_movies[['title', 'popularity', 'vote_average', 'release_date', 'genres']].to_dict(
            orient='records')

        # Render recommendations
        return render(request, 'recommendation.html', {
            'movies': recommended_movies,
            'selected_genres': selected_genres
        })

    # Default render for GET requests (optional)
    return render(request, 'recommend_form.html')

