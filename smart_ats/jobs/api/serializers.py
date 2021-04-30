from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from smart_ats.companies.models import Company
from smart_ats.jobs.models import Category, Job
from smart_ats.users.api.serializers import SimpleUserSerializer


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
