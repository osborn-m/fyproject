import json
from datetime import datetime
from django.core.management.base import BaseCommand
from universities.models import University, Program, Facility

class Command(BaseCommand):
    help = "Import universities from a JSON file"

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
                # Basic fields
                name = entry.get("name")
                type_ = entry.get("type", "")
                founded = entry.get("founded", 0)
                location = entry.get("location", "")
                description = entry.get("description", "")

                # Contact
                contact = entry.get("contact", {})
                contact_address = contact.get("address", "")
                contact_phone = contact.get("phone", "")
                contact_email = contact.get("email", "")
                contact_website = contact.get("website", "")

                # Rankings
                rankings = entry.get("rankings", {})
                national_rank = rankings.get("national_rank")

                # Statistics
                statistics = entry.get("statistics", {})
                total_students = statistics.get("total_students")
                student_to_faculty_ratio = statistics.get("student_to_faculty_ratio")

                # Admissions
                admissions = entry.get("admissions", {})
                application_deadline_str = admissions.get("application_deadline")
                application_deadline = None
                if application_deadline_str:
                    try:
                        application_deadline = datetime.strptime(application_deadline_str, "%Y-%m-%d").date()
                    except:
                        pass

                # Tuition Fees
                tuition = entry.get("tuition_fees", {})
                domestic = tuition.get("domestic_undergraduate", {})
                international = tuition.get("international_undergraduate", {})
                accommodation = tuition.get("accommodation", {})

                university, created = University.objects.update_or_create(
                    name=name,
                    defaults={
                        "type": type_,
                        "founded": founded,
                        "location": location,
                        "description": description,
                        "contact_address": contact_address,
                        "contact_phone": contact_phone,
                        "contact_email": contact_email,
                        "contact_website": contact_website,
                        "national_rank": national_rank,
                        "total_students": total_students,
                        "student_to_faculty_ratio": student_to_faculty_ratio,
                        "application_deadline": application_deadline,
                        "domestic_undergraduate_min": domestic.get("min"),
                        "domestic_undergraduate_max": domestic.get("max"),
                        "domestic_currency": domestic.get("currency", "GHS"),
                        "international_undergraduate_min": international.get("min"),
                        "international_undergraduate_max": international.get("max"),
                        "international_currency": international.get("currency", "USD"),
                        "accommodation_min": accommodation.get("min"),
                        "accommodation_max": accommodation.get("max"),
                        "accommodation_currency": accommodation.get("currency", "GHS"),
                    }
                )

                # Programs
                programs = entry.get("programs", [])
                for prog in programs:
                    Program.objects.update_or_create(
                        university=university,
                        name=prog.get("name", "Unnamed Program"),
                        defaults={
                            "cutoff_points": prog.get("cutoff_points", "15"),
                            "requirements": prog.get("requirements", "Standard requirements")
                        }
                    )

                imported_count += 1

            except Exception as e:
                skipped_count += 1
                self.stderr.write(self.style.WARNING(f"Skipped {name} due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} universities. Skipped {skipped_count} entries."))
