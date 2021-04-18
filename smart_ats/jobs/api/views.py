from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Job
from .permissions import IsJobAuthorOrReadOnly
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsJobAuthorOrReadOnly]

    @action(detail=True, methods=["patch"])
    def activate(self, request, pk=None):
        job = self.get_object()
        job.activate()
        job.save()
        return Response({"detail": "Job Activated"})

    @action(detail=True, methods=["patch"])
    def archive(self, request, pk=None):
        job = self.get_object()
        job.archive()
        job.save()
        return Response({"detail": "Job Archived"})
