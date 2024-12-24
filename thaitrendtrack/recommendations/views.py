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


# @csrf_exempt
# def recommend(request):
#     if request.method == "POST":
#         # Get user-selected genres
#         selected_genres = request.POST.getlist('genres')
#         print(selected_genres)
#
#         # Load the CSV file
#         csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Update the path to your file
#         movies_df = pd.read_csv(csv_path)
#
#         # Filter movies based on selected genres
#         def genre_filter(genres):
#             return any(genre in genres for genre in selected_genres)
#
#         filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]
#
#         # Sort movies by popularity and vote_average
#         sorted_movies = filtered_movies.sort_values(
#             by=['popularity', 'vote_average'], ascending=[False, False]
#         )
#
#         # Get movie titles
#         recommended_titles = sorted_movies['title'].tolist()
#
#         # Render results to a template
#         return render(request, 'recommendation.html', {'movies': recommended_titles})
#
#     return render(request, 'preference.html')

@csrf_exempt
def recommend(request):
    if request.method == "POST":
        # Get user-selected genres
        selected_genres = request.POST.getlist('genres')

        # Print the selected genres to the console
        print("Selected Genres:", selected_genres)

        # Load the CSV file
        csv_path = "get_databased/thai_movies_all_with_genres.csv"  # Update the path to your file
        movies_df = pd.read_csv(csv_path)

        # Filter movies based on selected genres
        def genre_filter(genres):
            return any(genre in genres for genre in selected_genres)

        filtered_movies = movies_df[movies_df['genres'].apply(genre_filter)]

        # Sort movies by popularity and vote_average
        sorted_movies = filtered_movies.sort_values(
            by=['popularity', 'vote_average'], ascending=[False, False]
        )

        # Get movie titles
        recommended_titles = sorted_movies['title'].tolist()

        # Render results to a template and pass selected genres along with recommended titles
        return render(request, 'recommendation.html', {
            'movies': recommended_titles,
            'selected_genres': selected_genres
        })

    return render(request, 'preference.html')
 