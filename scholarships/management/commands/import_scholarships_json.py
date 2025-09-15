import json
from datetime import datetime
from django.core.management.base import BaseCommand
from scholarships.models import Scholarship

class Command(BaseCommand):
    help = "Import scholarships from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--file",
            type=str,
            required=True,
            help="Path to the JSON file to import"
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to load JSON file: {e}"))
            return

        imported_count = 0
        skipped_count = 0

        for entry in data:
            try:
                # Map JSON fields to Scholarship model
                scholarship_name = entry.get("name", "Unnamed Scholarship")
                sponsor = entry.get("sponsor", "Unknown Sponsor")
                category = entry.get("category", "Other")
                level = entry.get("level", "Other")
                description = entry.get("description", "")
                
                # Application deadline
                deadline_str = entry.get("admissions", {}).get("application_deadline")
                application_deadline = None
                if deadline_str:
                    try:
                        application_deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                    except Exception:
                        pass

                # Eligibility, benefits, application process
                eligibility_requirements = entry.get("eligibility_requirements", [])
                benefits = entry.get("benefits", [])
                application_process = entry.get("application_process", [])

                # Contact / website
                contact = entry.get("contact", {})
                website_or_contact = contact.get("website", "")

                # Amount & application_url
                tuition = entry.get("tuition_fees", {})
                domestic = tuition.get("domestic_undergraduate", {})
                amount = f"{domestic.get('min', '')} - {domestic.get('max', '')} {domestic.get('currency', '')}" if domestic else None
                application_url = contact.get("website", "")

                # Create or update scholarship
                Scholarship.objects.update_or_create(
                    scholarship_name=scholarship_name,
                    defaults={
                        "sponsor": sponsor,
                        "category": category,
                        "level": level,
                        "description": description,
                        "application_deadline": application_deadline,
                        "eligibility_requirements": eligibility_requirements,
                        "benefits": benefits,
                        "application_process": application_process,
                        "website_or_contact": website_or_contact,
                        "amount": amount,
                        "application_url": application_url
                    }
                )
                imported_count += 1

            except Exception as e:
                skipped_count += 1
                self.stderr.write(self.style.WARNING(f"Skipped {entry.get('name')} due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} scholarships. Skipped {skipped_count} entries."))
