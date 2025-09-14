import json
from django.core.management.base import BaseCommand
from schools.models import School, Program, Facility

class Command(BaseCommand):
    help = "Import schools from a JSON file with default programs, facilities, and residency"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        file_path = options["json_file"]

        # Read JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # If file contains a single object, wrap it in a list
        if isinstance(data, dict):
            data = [data]

        for item in data:
            school_name = item.get("School")
            if not school_name:
                self.stdout.write(self.style.WARNING("Skipping entry with no school name"))
                continue

            # Clean "Passed %" value
            passed_value = item.get("Passed %", 0)
            if isinstance(passed_value, str):
                passed_value = passed_value.replace("%", "").strip()
                passed_value = int(passed_value) if passed_value.isdigit() else 0
            elif passed_value is None:
                passed_value = 0

            # Create or update school
            school, created = School.objects.get_or_create(
                name=school_name,
                defaults={
                    "region": item.get("Region", ""),
                    "district": item.get("District", ""),
                    "passed": passed_value,
                    "residency": "Boarding",  # Default for all
                    "gender": item.get("Gender", None),
                    "description": "",
                    "wassce_ranking": item.get("S.N", None),
                    "address": f"{school_name}, {item.get('District', '')}, {item.get('Region', '')}, Ghana",
                    "email": (
                        item.get("Email", "Contact the school administration")
                        or "Contact the school administration"
                    ),
                }
            )

            # Programs: assign defaults for all schools
            default_programs = ["Agriculture", "Business", "Visual Arts", "General Science", "General Arts"]
            gender = (item.get("Gender") or "").lower()
            if gender in ["mixed", "female", "girls"]:
                default_programs.append("Home Economics")

            program_objs = [Program.objects.get_or_create(name=prog)[0] for prog in default_programs]
            school.programs.set(program_objs)

            # Facilities: assign all
            all_facilities = ["Classrooms", "Library", "Science Labs", "Computer Lab", "Sports Facilities"]
            facility_objs = [Facility.objects.get_or_create(name=fac)[0] for fac in all_facilities]
            school.facilities.set(facility_objs)

            school.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {school_name} with default settings"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {school_name} with default settings"))
