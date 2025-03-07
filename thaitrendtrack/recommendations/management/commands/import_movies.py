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

# from django.core.management.base import BaseCommand
# import pandas as pd
# from recommendations.models import Movie
#
# class Command(BaseCommand):
#     help = 'Load movies from CSV into the database'
#
#     def handle(self, *args, **kwargs):
#         csv_path = "get_databased/thai_movies_with_titles_and_posters.csv"
#
#         try:
#             # Load movie data from CSV
#             movies_df = pd.read_csv(csv_path).fillna('')  # Fill NaN with empty strings
#
#             movie_objects = []  # List to hold movie instances
#
#             for _, row in movies_df.iterrows():
#                 # Ensure genres are stored correctly as a string
#                 genres = row['genres']
#                 if isinstance(genres, str):
#                     genre_list = [genre.strip() for genre in genres.split(',')]
#                 else:
#                     genre_list = []
#
#                 genres_string = ", ".join(genre_list)  # Convert list to string
#
#                 # Parse release_date safely
#                 try:
#                     release_date = pd.to_datetime(row['release_date'], errors='coerce')
#                     release_date = release_date.date() if pd.notna(release_date) else None
#                 except Exception as e:
#                     print(f"Error parsing release_date: {row['release_date']} - {e}")
#                     release_date = None
#
#                 # Create movie object (but don't save yet)
#                 movie_objects.append(
#                     Movie(
#                         title_en=row['english_title'],
#                         title_th=row['thai_title'],
#                         release_date=release_date,
#                         genres=genres_string,  # ✅ Stored as a clean string
#                         description=row['overview'],
#                         poster_path=row['poster_path'],
#                         runtime=None,  # Can be updated later
#                         popularity=row['popularity'],
#                         vote_average=row['vote_average']
#                     )
#                 )
#
#             # Bulk insert movies for efficiency
#             if movie_objects:
#                 Movie.objects.bulk_create(movie_objects)
#                 self.stdout.write(self.style.SUCCESS(f'{len(movie_objects)} movies imported successfully'))
#             else:
#                 self.stdout.write(self.style.WARNING('No movies found to import'))
#
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

# import json
# import csv
# from datetime import datetime
# from django.core.management.base import BaseCommand
# from recommendations.models import Movie  # Ensure correct import
#
# class Command(BaseCommand):
#     help = "Import movies from CSV into the database"
#
#     def safe_json_loads(self, data, default_value):
#         """Safely parse JSON or return a default value if data is invalid."""
#         if isinstance(data, (dict, list)):  # ✅ If already a dictionary/list, return as-is
#             return data
#         if isinstance(data, str) and data.strip() and data not in ["N/A", ""]:
#             try:
#                 return json.loads(data)
#             except json.JSONDecodeError:
#                 return default_value
#         return default_value
#
#     def handle(self, *args, **kwargs):
#         csv_file = "get_databased/thai_movies_and_tv.csv"  # ✅ Ensure correct path
#
#         with open(csv_file, newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     # ✅ Ensure 'genres' is a list
#                     genres = row['genres'].split(", ") if isinstance(row.get('genres'), str) and row['genres'].strip() not in ["N/A", ""] else []
#
#                     # ✅ Fix 'cast' (Ensure it's always a list before processing)
#                     cast_list = []
#                     cast_data = row.get('cast', "")
#
#                     if isinstance(cast_data, str):  # ✅ If it's a string, process it normally
#                         if cast_data.strip() not in ["N/A", ""]:
#                             cast_entries = cast_data.split(", ")
#                             for entry in cast_entries:
#                                 entry = entry.strip()
#                                 if " (" in entry and entry.endswith(")"):
#                                     name, img_url = entry.rsplit(" (", 1)
#                                     img_url = img_url.rstrip(")")
#                                     if img_url == "N/A":
#                                         img_url = "https://via.placeholder.com/100"  # Default image
#                                 else:
#                                     name, img_url = entry, "https://via.placeholder.com/100"
#                                 cast_list.append({"name": name.strip(), "image": img_url.strip()})
#                     elif isinstance(cast_data, list):  # ✅ If it's already a list, keep it
#                         cast_list = cast_data
#                     else:
#                         cast_list = []
#
#                     # ✅ Ensure 'watch_platforms' is always a dictionary
#                     watch_platforms = self.safe_json_loads(row.get('watch_platforms', "{}"), {})
#
#                     # ✅ Fix 'release_date' (Handle empty or incorrect format)
#                     release_date = row.get('release_date', "").strip()
#                     if release_date and release_date not in ["N/A", ""]:
#                         try:
#                             release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
#                         except ValueError:
#                             self.stdout.write(self.style.WARNING(f"⚠️ Invalid date format: {release_date}, setting to NULL"))
#                             release_date = None
#                     else:
#                         release_date = None
#
#                     # ✅ Ensure 'poster_path' is always a valid URL
#                     poster_path = row.get('poster_path', "").strip()
#                     if not poster_path or poster_path in ["N/A", ""]:
#                         poster_path = "https://via.placeholder.com/300"
#
#                     # ✅ Import movie into Django database
#                     movie, created = Movie.objects.update_or_create(
#                         id=row['id'],
#                         defaults={
#                             'title_th': row['thai_title'],
#                             'title_en': row['english_title'],
#                             'original_title': row['original_title'],
#                             'genres': genres,
#                             'status': row['status'],
#                             'release_date': release_date,
#                             'cast': cast_list,  # ✅ Ensured cast is always a list
#                             'watch_platforms': watch_platforms,  # ✅ Ensured watch_platforms is a dictionary
#                             'content_type': row['content_type'],
#                             'poster_path': poster_path
#                         }
#                     )
#
#                     if created:
#                         self.stdout.write(self.style.SUCCESS(f"✅ Added: {movie.title_en}"))
#                     else:
#                         self.stdout.write(self.style.WARNING(f"🔄 Updated: {movie.title_en}"))
#
#                 except KeyError as e:
#                     self.stdout.write(self.style.ERROR(f"❌ Missing key: {e} in row {row}"))
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"❌ Unexpected error in row {row}: {e}"))

import json
import csv
import json
from django.core.management.base import BaseCommand
from recommendations.models import Movie  # Replace 'recommendations' with your actual app name

class Command(BaseCommand):
    help = "Import movies from CSV"

    def parse_watch_platforms(self, watch_platforms):
        """
        Convert semicolon-separated watch platform data into a JSON dictionary.
        Example:
        "AD: Netflix; AE: Netflix, Netflix Basic with Ads"
        →
        {"AD": {"streaming": ["Netflix"]}, "AE": {"streaming": ["Netflix", "Netflix Basic with Ads"]}}
        """
        if not watch_platforms or watch_platforms.lower() == "n/a":
            return {}

        platforms_dict = {}
        try:
            entries = watch_platforms.split(";")  # Split by semicolon
            for entry in entries:
                parts = entry.split(":")
                if len(parts) == 2:
                    country = parts[0].strip()
                    services = [s.strip() for s in parts[1].split(",")]
                    platforms_dict[country] = {"streaming": services}
            return platforms_dict
        except Exception as e:
            print(f"❌ Error parsing watch_platforms: {watch_platforms} → {e}")
            return {}

    def handle(self, *args, **kwargs):
        csv_file_path = "get_databased/thai_movies_and_tv_series.csv"  # Ensure this path is correct

        try:
            with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        # ✅ Handle missing columns with `.get()`
                        genres = row.get("genres", "").split(",") if row.get("genres") else []
                        cast = row.get("cast", "").split(",") if row.get("cast") else []
                        status = row.get("status", "Unknown").strip()
                        runtime = None # Handle missing runtime safely

                        # ✅ Convert semicolon-separated watch_platforms to JSON
                        watch_platforms_raw = row.get("watch_platforms", "").strip()
                        watch_platforms = self.parse_watch_platforms(watch_platforms_raw)

                        # ✅ Convert numerical fields safely
                        try:
                            popularity = float(row.get("popularity", 0)) if row.get("popularity") else None
                        except ValueError:
                            print(f"⚠️ Warning: Invalid popularity value -> {row.get('popularity')}")
                            popularity = None  # Default to None

                        try:
                            vote_average = float(row.get("vote_average", 0)) if row.get("vote_average") else None
                        except ValueError:
                            print(f"⚠️ Warning: Invalid vote_average value -> {row.get('vote_average')}")
                            vote_average = None  # Default to None

                        # ✅ Convert release_date safely
                        release_date = row.get("release_date") if row.get("release_date") else None

                        # ✅ Create or update movie record
                        movie, created = Movie.objects.get_or_create(
                            title_th=row.get("thai_title", ""),
                            title_en=row.get("english_title", ""),
                            original_title=row.get("original_title", ""),
                            genres=genres,
                            status=status,
                            release_date=release_date,
                            poster_path=row.get("poster_path", ""),
                            cast=cast,
                            watch_platforms=watch_platforms,
                            content_type=row.get("content_type", ""),
                            popularity=popularity,
                            vote_average=vote_average,
                            runtime=runtime,  # Fixed KeyError issue
                        )

                        if created:
                            print(f"✅ Added: {movie.title_en}")
                        else:
                            print(f"🔄 Updated: {movie.title_en}")

                    except Exception as e:
                        print(f"❌ Error processing row {row}: {e}")

        except FileNotFoundError:
            print(f"❌ CSV file '{csv_file_path}' not found! Make sure it's in the project root directory.")
