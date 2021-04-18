from rest_framework import serializers
from smart_ats.jobs.models import Job


class JobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'category', 'company', 'author', 'state')


    
