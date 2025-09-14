from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Scholarship
from .serializers import ScholarshipSerializer

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [AllowAny]  # <-- make API public
