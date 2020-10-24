from rest_framework import viewsets

from smart_ats.companies.models import Company

from .permissions import IsCompanyAdminOrReadOnly
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsCompanyAdminOrReadOnly,)
