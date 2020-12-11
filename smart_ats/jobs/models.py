from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from smart_ats.companies.models import Company, CompanyAdmin
from taggit.managers import TaggableManager


class Category(TimeStampedModel):
    title = models.CharField(max_length=30, db_index=True)


class Job(TimeStampedModel):
    STATUS = Choices(('Active', _('Active')), ('Draft', _('Draft')), ('Archived', _('Archived')))

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(CompanyAdmin, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS.Archived)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name} {self.company.name} {self.author.name}'
