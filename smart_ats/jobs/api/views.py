from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsJobCompanyAdminOrReadOnly
from .serializers import *


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsJobCompanyAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return JobSerializer
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
