from django.core.management.base import BaseCommand
from recommendations.models import Community

class Command(BaseCommand):
    help = 'Insert default communities into the database'

    def handle(self, *args, **kwargs):
        communities = [
            {"name": "Action Club", "description": "A community for action movie lovers"},
            {"name": "Comedy Club", "description": "A community for comedy movie lovers"},
            {"name": "Crime Club", "description": "A community for crime movie lovers"},
            {"name": "Drama Club", "description": "A community for drama movie lovers"},
            {"name": "Horror Club", "description": "A community for horror movie lovers"},
            {"name": "Romance Club", "description": "A community for romance movie lovers"},
        ]

        for community in communities:
            Community.objects.create(name=community["name"], description=community["description"])

        self.stdout.write(self.style.SUCCESS('Successfully inserted default communities!'))
