from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from smart_ats.companies.models import Company

from .permissions import IsJobCompanyAdminOrReadOnly
from .serializers import JobSerializer, JobWriterSerializer


class JobViewSet(viewsets.ModelViewSet):
    permission_classes = (IsJobCompanyAdminOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Company, id=self.kwargs["company_id"]).job_set.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
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
