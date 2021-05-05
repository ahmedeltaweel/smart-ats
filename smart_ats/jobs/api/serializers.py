from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from smart_ats.companies.models import Company
from smart_ats.jobs.models import Category, Job, JobApplication
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
            "state",
            "author",
            "company",
            "tags",
        ]
        read_only_fields = ("author", "company")

    def create(self, validated_data):
        validated_data["company_id"] = int(self.context["view"].kwargs["company_id"])
        validated_data["author"] = self.context["request"].user.companyadmin
        return super().create(validated_data)


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
    class Meta:
        model = JobApplication
        fields = [
            "data",
            "cv_url",
            "state",
            "user",
            "job",
        ]
        read_only_fields = ("state", "user", "job")

    def create(self, validated_data):
        validated_data["job_id"] = int(self.context["view"].kwargs["job_id"])
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
