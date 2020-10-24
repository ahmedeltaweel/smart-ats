from rest_framework import permissions


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not obj.company_admin:
            return False
        return obj.company_admin == request.user
