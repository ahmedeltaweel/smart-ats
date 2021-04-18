from rest_framework import permissions, viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from smart_ats.jobs.models import Job

from .permissions import UpdateOwnJob
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = (
        UpdateOwnJob,
        IsAuthenticated
        )
   
