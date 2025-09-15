import json
from django.core.management.base import BaseCommand
from schools.models import School

class Command(BaseCommand):
    help = "Import schools from a JSON file"

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
            # Normalize keys: remove spaces and lowercase
            fields = {k.lower().replace(" ", "_"): v for k, v in entry.items()}

            name = fields.get("school")
            region = fields.get("region", "")
            district = fields.get("district", "")
            passed_str = fields.get("passed_%", "0")
            try:
                passed = int(passed_str.replace("%", "").strip())
            except:
                passed = 0
            residency_raw = fields.get("residency", "")
            if "Day" in residency_raw:
                residency = "Day"
            elif "Boarding" in residency_raw:
                residency = "Boarding"
            else:
                residency = "Day"  # default
            gender = fields.get("gender", None)
            email = fields.get("email", "Contact the school administration")

            if not name:
                self.stdout.write(self.style.WARNING(f"Skipping row with missing school name: {fields}"))
                skipped_count += 1
                continue

            school, created = School.objects.update_or_create(
                name=name,
                defaults={
                    "region": region,
                    "district": district,
                    "passed": passed,
                    "residency": residency,
                    "gender": gender,
                    "email": email
                }
            )

            imported_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} schools. Skipped {skipped_count} rows."))
