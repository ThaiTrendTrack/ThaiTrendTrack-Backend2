# from django.core.management.base import BaseCommand
# import pandas as pd
# from recommendations.models import Movie
#
#
# class Command(BaseCommand):
#     help = 'Load movies from CSV into the database'
#
#     def handle(self, *args, **kwargs):
#         csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"
#         try:
#             # Read the CSV data
#             movies_df = pd.read_csv(csv_path)
#
#             # Iterate through the CSV data and add it to the database
#             for index, row in movies_df.iterrows():
#                 genres = row['genres']
#
#                 # Check if genres is a string before splitting
#                 if isinstance(genres, str):
#                     genre_list = genres.split(', ')  # Split the string by commas
#                 else:
#                     genre_list = []  # If it's not a string, set genres to an empty list
#
#                 # Parse release_date manually if it's a valid string
#                 try:
#                     # Attempt to convert release_date to datetime
#                     release_date = pd.to_datetime(row['release_date'], errors='coerce')
#
#                     # If release_date is NaT, set it to None
#                     if pd.isna(release_date):
#                         release_date = None
#                     else:
#                         release_date = release_date.date()  # Convert to date type
#                 except Exception as e:
#                     print(f"Error parsing release_date: {row['release_date']} - {e}")
#                     release_date = None  # Set to None if the date can't be parsed
#
#                 # Create the movie entry in the database
#                 Movie.objects.create(
#                     title_en=row['english_title'],  # Use the correct column name
#                     title_th=row['thai_title'],  # Use the correct column name
#                     release_date=release_date,  # Use the parsed date
#                     genres=genre_list,  # Use the generated genre list
#                     description=row['overview'],  # Use the correct column name
#                     poster_path=row['poster_path'],
#                     runtime=None,
#                     popularity=row['popularity'],  # Add popularity data if available
#                     vote_average=row['vote_average']
#
#                 )
#
#             self.stdout.write(self.style.SUCCESS('Movies imported successfully'))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

from django.core.management.base import BaseCommand
import pandas as pd
from recommendations.models import Movie

class Command(BaseCommand):
    help = 'Load movies from CSV into the database'

    def handle(self, *args, **kwargs):
        csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"

        try:
            # Load movie data from CSV
            movies_df = pd.read_csv(csv_path).fillna('')  # Fill NaN with empty strings

            movie_objects = []  # List to hold movie instances

            for _, row in movies_df.iterrows():
                # Ensure genres are stored correctly as a string
                genres = row['genres']
                if isinstance(genres, str):
                    genre_list = [genre.strip() for genre in genres.split(',')]
                else:
                    genre_list = []

                genres_string = ", ".join(genre_list)  # Convert list to string

                # Parse release_date safely
                try:
                    release_date = pd.to_datetime(row['release_date'], errors='coerce')
                    release_date = release_date.date() if pd.notna(release_date) else None
                except Exception as e:
                    print(f"Error parsing release_date: {row['release_date']} - {e}")
                    release_date = None

                # Create movie object (but don't save yet)
                movie_objects.append(
                    Movie(
                        title_en=row['english_title'],
                        title_th=row['thai_title'],
                        release_date=release_date,
                        genres=genres_string,  # ✅ Stored as a clean string
                        description=row['overview'],
                        poster_path=row['poster_path'],
                        runtime=None,  # Can be updated later
                        popularity=row['popularity'],
                        vote_average=row['vote_average']
                    )
                )

            # Bulk insert movies for efficiency
            if movie_objects:
                Movie.objects.bulk_create(movie_objects)
                self.stdout.write(self.style.SUCCESS(f'{len(movie_objects)} movies imported successfully'))
            else:
                self.stdout.write(self.style.WARNING('No movies found to import'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

