from rest_framework.permissions import IsAuthenticated

from smart_ats.companies.models import Company

from .permissions import IsCompanyAdminOrReadOnly
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (
        IsAuthenticated,
        IsCompanyAdminOrReadOnly,
    )
