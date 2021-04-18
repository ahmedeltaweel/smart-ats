from rest_framework import serializers

from smart_ats.jobs.models import Category, Job


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class JobWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
