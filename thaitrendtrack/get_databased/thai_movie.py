# import requests
# import csv
#
# # Replace with your own TMDb API key
# API_KEY = '33b7e0a891dc3f77534d78102c3d1546'
#
# # Define the base URL for the TMDb API
# BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
#
# # Parameters for the API request
# params = {
#     'api_key': API_KEY,
#     'region': 'TH',
#     'language': 'th-TH',
#     'sort_by': 'popularity.desc',
#     'include_adult': 'false',
#     'page': 1
# }
#
#
# # Function to get genre mapping
# def get_genre_mapping(api_key):
#     genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=th-TH'
#     response = requests.get(genre_url)
#     if response.status_code == 200:
#         genres = response.json()['genres']
#         return {genre['id']: genre['name'] for genre in genres}
#     else:
#         print(f'Failed to retrieve genres: {response.status_code}')
#         return {}
#
#
# # Get the genre mapping
# genre_map = get_genre_mapping(API_KEY)
#
# # Open a CSV file to write the data
# with open('thai_movies_all_with_genres.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     # Write the header row for the CSV
#     writer.writerow(
#         ['movie_id', 'title', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'genres'])
#
#     # Initialize a variable to track total pages
#     total_pages = 1
#
#     # Loop through all the pages until we reach the last page
#     while params['page'] <= total_pages:
#         # Send a request to the TMDb API
#         response = requests.get(BASE_URL, params=params)
#
#         # Check if the request was successful
#         if response.status_code == 200:
#             data = response.json()
#             movies = data['results']
#
#             # Write movie details into the CSV
#             for movie in movies:
#                 # Get genre names from genre IDs
#                 genre_names = [genre_map.get(genre_id, '') for genre_id in movie['genre_ids']]
#                 genres = ', '.join(genre_names)  # Convert list to comma-separated string
#
#                 # Write movie details with genres into the CSV
#                 writer.writerow(
#                     [movie['id'], movie['title'], movie['overview'], movie['release_date'], movie['popularity'],
#                      movie['vote_average'], movie['vote_count'], genres])
#
#             # Update the total number of pages from the API response
#             total_pages = data['total_pages']
#
#             # Move to the next page
#             params['page'] += 1
#         else:
#             print(f'Failed to retrieve data: {response.status_code}')
#             break
#
# print('All Thai movies with genres have been saved to thai_movies_all_with_genres.csv')
import requests
import csv

# Replace with your own TMDb API key
API_KEY = '33b7e0a891dc3f77534d78102c3d1546'

# Define the base URL for the TMDb API
BASE_URL = 'https://api.themoviedb.org/3/discover/movie'

# Parameters for the API request
params = {
    'api_key': API_KEY,
    'region': 'TH',
    'language': 'th-TH',
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'with_original_language': 'th',  # Ensure movies in Thai
    'page': 1
}


# Function to get genre mapping
def get_genre_mapping(api_key):
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=th-TH'
    response = requests.get(genre_url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['id']: genre['name'] for genre in genres}
    else:
        print(f'Failed to retrieve genres: {response.status_code} - {response.text}')
        return {}


# Get the genre mapping
genre_map = get_genre_mapping(API_KEY)

# Open a CSV file to write the data
with open('thai_movies_all_with_genres.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row for the CSV
    writer.writerow(
        ['movie_id', 'title', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'genres'])

    # Loop through all the pages until we reach the last page
    while True:
        # Send a request to the TMDb API
        response = requests.get(BASE_URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            total_pages = data.get('total_pages', 1)  # Get total pages from the API response

            # Write movie details into the CSV
            for movie in movies:
                # Get genre names from genre IDs
                genre_names = [genre_map.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])]
                genres = ', '.join(genre_names)  # Convert list to comma-separated string

                # Write movie details with genres into the CSV
                writer.writerow([
                    movie.get('id', 'N/A'),
                    movie.get('title', 'N/A'),
                    movie.get('overview', 'N/A'),
                    movie.get('release_date', 'N/A'),
                    movie.get('popularity', 'N/A'),
                    movie.get('vote_average', 'N/A'),
                    movie.get('vote_count', 'N/A'),
                    genres
                ])

            # Check if we have reached the last page
            if params['page'] >= total_pages:
                break

            # Move to the next page
            params['page'] += 1
        else:
            print(f'Failed to retrieve data on page {params["page"]}: {response.status_code} - {response.text}')
            break

print('All Thai movies with genres have been saved to thai_movies_all_with_genres.csv')
