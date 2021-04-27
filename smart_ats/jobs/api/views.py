from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from smart_ats.jobs.models import Job

from .permissions import IsJobCompanyAdminOrReadOnly
from .serializers import JobSerializer, JobWriterSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsAuthenticated, IsJobCompanyAdminOrReadOnly)

    def get_serializer(self):
        if self.action in ["list", "retrieve"]:
            return JobSerializer
        elif self.action in ["create", "update"]:
            return JobWriterSerializer

    @action(detail=True, methods=["PATCH"])
    def activate(self, request, pk=None):
        job = self.get_object()
        job.activate()
        job.save()
        return Response({"message": "Ok"})

    @action(detail=True, methods=["PATCH"])
    def archive(self, request, pk=None):
        job = self.get_object()
        job.archive()
        job.save()
        return Response({"message": "Ok"})
