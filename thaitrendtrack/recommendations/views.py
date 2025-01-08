import pandas as pd
from django.shortcuts import render, redirect
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


def preferences(request):
    if request.method == "POST":
        # Extract selected preferences from POST data
        selected_preferences = request.POST.getlist('genres[]')

        # Save preferences to the session
        request.session['preferences'] = selected_preferences

        # Redirect to the recommendations page
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
