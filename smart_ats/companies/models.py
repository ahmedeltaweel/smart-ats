from django.db import models
from model_utils.models import TimeStampedModel

from smart_ats.users.models import User


class CompanyAdmin(User):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Company Admin"
        verbose_name_plural = "Company Admins"


class Company(TimeStampedModel):
    name = models.CharField(max_length=15, blank=False, null=False)
    website = models.URLField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
