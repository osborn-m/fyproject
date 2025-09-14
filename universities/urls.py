from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityViewSet, FacilityViewSet, ProgramViewSet

router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='universities')
router.register(r'facilities', FacilityViewSet, basename='facilities')
router.register(r'programs', ProgramViewSet, basename='programs')

urlpatterns = [
    path('', include(router.urls)),
]
