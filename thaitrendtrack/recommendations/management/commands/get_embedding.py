from django.core.management.base import BaseCommand
from recommendations.models import Movie, get_embedding
import pickle


class Command(BaseCommand):
    help = 'Generates embeddings for movies and saves them to a file'

    def handle(self, *args, **kwargs):
        # Fetch all movies from the database
        movies = Movie.objects.all()

        # Generate embeddings for all movies
        embeddings = []
        for movie in movies:
            combined_text = f"{movie.title_th} {movie.title_en} {movie.overview} {movie.genres}"

            # Print the movie title currently being processed
            print(f"Processing movie: {movie.title_en} ({movie.title_th})")

            embedding_vector = get_embedding(combined_text)  # Generate embedding for the movie
            embeddings.append(embedding_vector)

        # Save embeddings to a pickle file
        with open('movie_embeddings.pkl', 'wb') as f:
            pickle.dump(embeddings, f)

        self.stdout.write(self.style.SUCCESS('Embeddings file "movie_embeddings.pkl" has been generated successfully!'))
