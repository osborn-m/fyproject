import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from scholarships.models import Scholarship

class Command(BaseCommand):
    help = "Import scholarships from scholarships.json"

    def handle(self, *args, **kwargs):
        file_path = "scholarships.json"  # Make sure this path is correct

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                scholarship, created = Scholarship.objects.update_or_create(
                    scholarship_name=item.get("scholarship_name"),
                    defaults={
                        "sponsor": item.get("sponsor"),
                        "category": item.get("category"),
                        "level": item.get("level"),
                        "description": item.get("description"),
                        "application_deadline": parse_date(item.get("application_deadline")),
                        "eligibility_requirements": item.get("eligibility_requirements", []),
                        "benefits": item.get("benefits", []),
                        "application_process": item.get("application_process", []),
                        "website_or_contact": item.get("website_or_contact"),
                        "amount": item.get("amount"),
                        "application_url": item.get("application_url"),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {scholarship.scholarship_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated: {scholarship.scholarship_name}"))

            self.stdout.write(self.style.SUCCESS("All scholarships imported successfully."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Invalid JSON: {e}"))
