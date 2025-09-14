from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import School, Program, SchoolCourse
@receiver(m2m_changed, sender=School.programs.through)
def school_programs_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        for program in instance.programs.all():
            for course in program.courses.all():
                if not SchoolCourse.objects.filter(
                    school=instance,
                    name=course.name
                ).exists():
                    SchoolCourse.objects.create(
                        school=instance,
                        name=course.name
                    )

                
    if action == "post_remove":
        SchoolCourse.objects.filter(
            school=instance, source_program__pk__in=pk_set, is_custom=False
        ).delete()
