from django.shortcuts import get_object_or_404
from rest_framework import permissions

from smart_ats.companies.models import CompanyAdmin
from smart_ats.jobs.models import Job


class IsJobCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(request.user, "companyadmin"):
            return False
        return request.user.companyadmin in CompanyAdmin.objects.filter(
            company_id=view.kwargs["company_id"]
        )


class IsApplicantOrJobCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        job = get_object_or_404(Job, id=view.kwargs["job_id"])
        if request.method == "POST":
            return job.state == Job.STATUS.ACTIVE
        if not hasattr(request.user, "companyadmin"):
            return False
        return request.user.companyadmin in CompanyAdmin.objects.filter(
            company_id=job.company_id
        )
