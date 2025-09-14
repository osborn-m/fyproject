import json
from django.core.management.base import BaseCommand
from universities.models import University, Program

class Command(BaseCommand):
    help = 'Import universities from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to the JSON file containing universities data'
        )

    def handle(self, *args, **options):
        file_path = options['json_file']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                universities = json.load(f)

            for uni_data in universities:
                university, created = University.objects.get_or_create(
                    name=uni_data['name'],
                    defaults={
    'type': uni_data.get('type', 'Public'),
    'founded': uni_data.get('founded'),
    'location': uni_data.get('location', ''),
    'description': uni_data.get('description', ''),
    'national_rank': uni_data.get('rankings', {}).get('national_rank'),
    'total_students': uni_data.get('statistics', {}).get('total_students'),
    'student_to_faculty_ratio': uni_data.get('statistics', {}).get('student_to_faculty_ratio', ''),
    'application_deadline': uni_data.get('admissions', {}).get('application_deadline', ''),
    'domestic_undergraduate_min': uni_data.get('tuition_fees', {}).get('domestic_undergraduate', {}).get('min', 0),
    'domestic_undergraduate_max': uni_data.get('tuition_fees', {}).get('domestic_undergraduate', {}).get('max', 0),
    'international_undergraduate_min': uni_data.get('tuition_fees', {}).get('international_undergraduate', {}).get('min', 0),
    'international_undergraduate_max': uni_data.get('tuition_fees', {}).get('international_undergraduate', {}).get('max', 0),
    'accommodation_min': uni_data.get('tuition_fees', {}).get('accommodation', {}).get('min', 0),
    'accommodation_max': uni_data.get('tuition_fees', {}).get('accommodation', {}).get('max', 0),
}

                )

                for program_data in uni_data.get('programs', []):
                    Program.objects.get_or_create(
                        university=university,
                        name=program_data['name'],
                        cutoff_points=program_data.get('cutoff_points', '15'),
                        requirements=program_data.get('requirements', 'Standard requirements')
                    )

            self.stdout.write(self.style.SUCCESS('Universities imported successfully!'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File '{file_path}' not found"))
