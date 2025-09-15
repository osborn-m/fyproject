import json
import os
from django.core.management.base import BaseCommand
from resources.models import Resource
from django.conf import settings

class Command(BaseCommand):
    help = 'Import resources from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--file', type=str, required=True,
            help='Path to the JSON file containing resources'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        # If the path is relative, assume it's relative to project root
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON decode error: {e}"))
            return

        for entry in data:
            name = entry.get('name')
            category = entry.get('category')
            file = entry.get('file')

            if not all([name, category, file]):
                self.stdout.write(self.style.WARNING(f"Skipping incomplete entry: {entry}"))
                continue

            resource, created = Resource.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'file': file
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created resource: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Resource already exists: {name}"))
