from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from smart_ats.companies.models import Company, CompanyAdmin
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from .managers import JobManager


class Category(MPTTModel):
    name = models.CharField(max_length=30, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='Children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return Category.name


class Job(TimeStampedModel):
    STATUS = Choices(('Active', _('Active')), ('Draft', _('Draft')), ('Archived', _('Archived')))

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(CompanyAdmin, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS.Draft)
    tags = TaggableManager()

    objects = JobManager()

    def __str__(self):
        return f'{self.title} {self.company.name} {self.author.first_name}'
