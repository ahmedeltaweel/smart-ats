from rest_framework import viewsets

from smart_ats.companies.models import Company

from .serializers import CompanySerializer

from . import permissions


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Company Api View
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]
