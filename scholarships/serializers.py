from rest_framework import serializers
from .models import Scholarship

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [
            "id",
            "scholarship_name",
            "sponsor",
            "category",
            "level",
            "description",
            "application_deadline",
            "eligibility_requirements",
            "benefits",
            "application_process",
            "website_or_contact",
            "amount",
            "application_url",
            "created_at",
            "updated_at"
        ]
