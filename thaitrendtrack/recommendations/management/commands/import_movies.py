import csv
import pickle
from django.core.management.base import BaseCommand
from recommendations.models import Movie


class Command(BaseCommand):
    help = "Import movies from CSV"

    def parse_watch_platforms(self, watch_platforms):
        """
        Convert semicolon-separated watch platform data into a JSON dictionary.
        Example:
        "AD: Netflix; AE: Netflix, Netflix Basic with Ads"
        → {"AD": {"streaming": ["Netflix"]}, "AE": {"streaming": ["Netflix", "Netflix Basic with Ads"]}}
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
        csv_file_path = "get_databased/thai_movies_and_tv_series_2.csv"  # Ensure this path is correct

        try:
            with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        # ✅ Handle missing columns with `.get()`
                        genres = row.get("genres", "").split(",") if row.get("genres") else []
                        cast = row.get("cast", "").split(",") if row.get("cast") else []
                        overview = row.get("overview", "").strip()  # ✅ Add overview
                        status = row.get("status", "Unknown").strip()
                        runtime = row.get("runtime", "").strip() if row.get("runtime") else None

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
                            overview=overview,  # ✅ Add overview
                            status=status,
                            release_date=release_date,
                            poster_path=row.get("poster_path", ""),
                            cast=cast,
                            watch_platforms=watch_platforms,
                            content_type=row.get("content_type", ""),
                            popularity=popularity,
                            vote_average=vote_average,
                            runtime=runtime,
                        )

                        # ✅ Update embedding (only if created new record)
                        if created or not movie.embedding:
                            movie.save()  # ✅ ใช้ `save()` เพื่อให้ Model คำนวณ embedding อัตโนมัติ

                        if created:
                            print(f"✅ Added: {movie.title_en}")
                        else:
                            print(f"🔄 Updated: {movie.title_en}")

                    except Exception as e:
                        print(f"❌ Error processing row {row}: {e}")

        except FileNotFoundError:
            print(f"❌ CSV file '{csv_file_path}' not found! Make sure it's in the correct directory.")
