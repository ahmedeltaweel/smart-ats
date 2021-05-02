from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from smart_ats.companies.models import Company
from smart_ats.jobs.models import Job

from .permissions import IsApplicantOrJobCompanyAdmin, IsJobCompanyAdminOrReadOnly
from .serializers import (
    JobApplicationSerializer,
    JobApplicationWriterSerializer,
    JobSerializer,
    JobWriterSerializer,
)


class JobViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsJobCompanyAdminOrReadOnly,
    )

    def get_queryset(self):
        try:
            company = Company.objects.get(id=self.kwargs["company_id"])
        except ObjectDoesNotExist:
            raise NotFound(detail="Company Does not exist")
        return company.job_set.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return JobSerializer
        return JobWriterSerializer

    @action(detail=True, methods=["PATCH"])
    def activate(self, request, pk=None, *args, **kwargs):
        job = self.get_object()
        job.activate()
        job.save()
        return Response({"message": "Ok"})

    @action(detail=True, methods=["PATCH"])
    def archive(self, request, pk=None, *args, **kwargs):
        job = self.get_object()
        job.archive()
        job.save()
        return Response({"message": "Ok"})


class JobApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsApplicantOrJobCompanyAdmin]

    def get_queryset(self):
        try:
            job = Job.objects.get(
                id=self.kwargs["job_id"], status=self.kwargs["Active"]
            )
        except ObjectDoesNotExist:
            raise NotFound(detail="Job Does not exist")
        return job.job_application.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return JobApplicationSerializer
        return JobApplicationWriterSerializer
