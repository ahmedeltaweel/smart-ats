from smart_ats.companies.models import User, CompanyAdmin
from rest_framework import permissions


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.user_type != User.statuses.admin:
            return False
    
        if request.method == "POST":
            if hasattr(request.user, CompanyAdmin):
                return False
        
        return True


    def has_object_permission(self, request, view, obj):
        
        if not hasattr(request.user, "companyadmin"):
            return False
       
        # update, delete
        return request.user.companyadmin in obj.company_admin.all()
