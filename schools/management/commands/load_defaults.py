from django.core.management.base import BaseCommand
from schools.models import Facility, Program, Course

class Command(BaseCommand):
    help = "Load default facilities, programs, and courses from the PDF"

    def handle(self, *args, **options):
        facilities = [
            "Classrooms", "Library", "Science Labs", "Computer Lab",
            "Sports Facilities", "Dining Hall", "Dormitories", "Assembly Hall"
        ]
        for f in facilities:
            Facility.objects.get_or_create(name=f)

        program_courses = {
            "General Arts": ["Economics", "Geography", "History", "Government"],
            "General Science": ["Chemistry", "Biology", "Physics", "Elective Mathematics", "Elective ICT (Computer Science)"],
            "Home Economics": ["Biology", "Management in living", "GKA - General Knowledge in Arts", "Economics", "Food and Nutrition"],
            "Visual Arts": ["Elective Mathematics", "GKA - General Knowledge in Arts", "Economics", "Graphic design", "Ceramics", "Leather work", "Sculpture", "Painting"],
            "Business": ["Elective Mathematics", "Economics", "Accounting", "Business Management (BM)", "Business Mathematics", "FINANCIAL ACCOUNTING"],
            "Agriculture": ["Animal Husbandry", "Chemistry", "General Agriculture", "Elective Mathematics"],
        }

        for p_name, courses in program_courses.items():
            program, _ = Program.objects.get_or_create(name=p_name)
            for c in courses:
                Course.objects.get_or_create(program=program, name=c)

        self.stdout.write(self.style.SUCCESS("Defaults loaded successfully"))
