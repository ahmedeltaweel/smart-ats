from django.db import models
from model_utils.models import TimeStampedModel

from smart_ats.users.models import User

from .managers import CompanyAdminManager


class CompanyAdmin(User):
    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name="company_admin"
    )

    objects = CompanyAdminManager()

    def __str__(self):
        return "Admin for: {}".format(self.company.name)


class Company(TimeStampedModel):
    name = models.CharField(max_length=15, blank=False, null=False)
    website = models.URLField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name
