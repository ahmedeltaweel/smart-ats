from rest_framework import serializers

from smart_ats.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False)

    class Meta:
        model = Company
        fields = ["id", "name", "website", "description", "address", "logo"]
