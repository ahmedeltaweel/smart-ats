from rest_framework import permissions


class IsJobAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(request.user, "companyadmin"):
            return False
        if request.method == "POST" and not obj:
            return True

        return request.user.companyadmin in obj.company.company_admin.all()
