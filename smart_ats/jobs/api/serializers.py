from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from smart_ats.companies.models import Company
from smart_ats.jobs.models import Category, Job

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


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
    company = CompanySerializer(many=False)
    category = CategorySerializer(many=False, read_only=True)
    author = UserSerializer(many=False)

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
