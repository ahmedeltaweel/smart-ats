from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from smart_ats.jobs.models import Job


class JobSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    category = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

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
