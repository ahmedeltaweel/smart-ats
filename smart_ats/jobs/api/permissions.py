from rest_framework import permissions

from smart_ats.companies.models import CompanyAdmin


class IsJobCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(request.user, "companyadmin"):
            return False
        return request.user.companyadmin in CompanyAdmin.objects.filter(
            company_id=view.kwargs["company_id"]
        )
