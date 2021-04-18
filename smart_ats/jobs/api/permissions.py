from rest_framework import permissions
from smart_ats.jobs.models import Job

class UpdateOwnJob(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
