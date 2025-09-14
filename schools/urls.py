from rest_framework import routers
from .views import SchoolViewSet, ProgramViewSet, FacilityViewSet, CourseViewSet, SchoolCourseViewSet

router = routers.DefaultRouter()
router.register(r"schools", SchoolViewSet)
router.register(r"programs", ProgramViewSet)
router.register(r"facilities", FacilityViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"school-courses", SchoolCourseViewSet)

urlpatterns = router.urls
