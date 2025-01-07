import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# def preferences(request):
#     if request.method == "POST":
#         # Extract selected preferences from POST data
#         selected_preferences = request.POST.getlist('preferences')
#
#         # Save or process preferences
#         request.session['preferences'] = selected_preferences
#
#         # Redirect to recommendations
#         return redirect('recommendations')
#
#     return render(request, 'preference.html')


# import pandas as pd
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
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
# @csrf_exempt
# def recommend(request):
#     if request.method == "POST":
#         # Get the user-selected genres
#         selected_genres = request.POST.getlist('genres[]')
#         selected_genres_thai = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]
#
#         # Load the movie dataset
#         csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Adjust the path as necessary
#         movies_df = pd.read_csv(csv_path)
#
#         # Ensure the 'genres' column is treated as a string and handle NaN values
#         movies_df['genres'] = movies_df['genres'].fillna('').astype(str)
#
#         # Filter movies based on selected genres
#         def genre_filter(genres):
#             return any(genre in genres for genre in selected_genres_thai)
#
#         filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]
#
#         # Sort movies by popularity, vote_average, and release_date
#         sorted_movies = filtered_movies.sort_values(
#             by=['popularity', 'vote_average', 'release_date'],
#             ascending=[False, False, False]
#         )
#
#         # Prepare movie data for the recommendation page
#         recommended_movies = sorted_movies[['title', 'popularity', 'vote_average', 'release_date', 'genres']].to_dict(
#             orient='records')
#
#         # Render recommendations
#         return render(request, 'recommendation.html', {
#             'movies': recommended_movies,
#             'selected_genres': selected_genres
#         })
#
#     # Default render for GET requests (optional)
#     return render(request, 'recommend_form.html')

# import pandas as pd
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
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
# def preferences(request):
#     if request.method == "POST":
#         # Extract selected preferences from POST data
#         selected_preferences = request.POST.getlist('genres[]')
#
#         # Save or process preferences
#         request.session['preferences'] = selected_preferences
#
#         # Redirect to recommendations
#         return redirect('recommend')
#
#     return render(request, 'preference.html')
#
# @csrf_exempt
# def recommend(request):
#     if request.method == "POST":
#         # Get the user-selected genres
#         selected_genres = request.POST.getlist('genres[]')
#         selected_genres_thai = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]
#
#         # Load the movie dataset
#         csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Adjust the path as necessary
#         movies_df = pd.read_csv(csv_path)
#
#         # Ensure the 'genres' column is treated as a string and handle NaN values
#         movies_df['genres'] = movies_df['genres'].fillna('').astype(str)
#
#         # Filter movies based on selected genres
#         def genre_filter(genres):
#             return any(genre in genres for genre in selected_genres_thai)
#
#         filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]
#
#         # Sort movies by popularity, vote_average, and release_date
#         sorted_movies = filtered_movies.sort_values(
#             by=['popularity', 'vote_average', 'release_date'],
#             ascending=[False, False, False]
#         )
#
#         # Prepare movie data for the recommendation page
#         recommended_movies = sorted_movies.to_dict(orient='records')
#
#         # Render the recommendation page with the data
#         return render(request, 'movies.html', {
#             'movies': recommended_movies,
#             'selected_genres': selected_genres,
#             'selected_genres_thai': selected_genres_thai
#         })
#
#     # If GET request, redirect to preference page
#     return redirect('preferences')

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
        selected_genres_thai = [GENRE_MAPPING.get(genre, genre) for genre in selected_genres]

        # Load movie data from the CSV file
        csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Adjust to the actual path
        try:
            movies_df = pd.read_csv(csv_path)

            # Handle missing or NaN values in 'genres'
            movies_df['genres'] = movies_df['genres'].fillna('').astype(str)

            # Filter movies that match the selected genres
            def genre_filter(genres):
                return any(genre in genres for genre in selected_genres_thai)

            filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]

            # Sort movies by popularity, vote_average, and release_date
            sorted_movies = filtered_movies.sort_values(
                by=['popularity', 'vote_average', 'release_date'],
                ascending=[False, False, False]
            )

            # Limit to the top 10 recommended movies
            recommended_movies = sorted_movies.head(10).to_dict(orient='records')

            # Render the movies.html page with the recommendations
            return render(request, 'movies.html', {
                'movies': recommended_movies,
                'selected_genres': selected_genres,
                'selected_genres_thai': selected_genres_thai
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



