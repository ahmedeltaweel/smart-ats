from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from smart_ats.companies.models import Company
from smart_ats.jobs.models import Category, Job, JobApplication
from smart_ats.users.api.serializers import SimpleUserSerializer

from .serializer_fields import CurrrentCompanyAdmin, CurrrentCompanyId, CurrrentJobId


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class JobSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    company = CompanySerializer()
    category = CategorySerializer()
    author = SimpleUserSerializer()

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "category",
            "company",
            "author",
            "state",
            "tags",
        ]


class JobWriterSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.HiddenField(default=CurrrentCompanyAdmin())
    company_id = serializers.HiddenField(default=CurrrentCompanyId())

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "category",
            "state",
            "author",
            "tags",
            "company_id",
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    job = JobSerializer()

    class Meta:
        model = JobApplication
        fields = [
            "user",
            "job",
            "state",
            "data",
            "cv_url",
        ]


class JobApplicationWriterSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    job_id = serializers.HiddenField(default=CurrrentJobId())

    class Meta:
        model = JobApplication
        fields = ["data", "cv_url", "user", "job_id"]
