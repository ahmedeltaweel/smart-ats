from rest_framework import permissions

from smart_ats.companies.models import Company


class IsJobCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(request.user, "companyadmin"):
            return False
        if request.method == "POST":
            return (
                request.user.companyadmin
                in Company.objects.get(id=request.POST["company"]).company_admin.all()
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.companyadmin in obj.company.company_admin.all():
            return True
        return False
