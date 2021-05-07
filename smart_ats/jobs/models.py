from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from smart_ats.companies.models import Company, CompanyAdmin
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from .managers import JobManager

from django_fsm import FSMField, transition


class Category(MPTTModel):
    name = models.CharField(max_length=30, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Job(TimeStampedModel):

    STATUS = Choices(
        ('DRAFT', _('Draft')),
        ('ACTIVE', _('Active')),
        ('ARCHIVED', _('Archived')),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(CompanyAdmin, on_delete=models.CASCADE)
    state = FSMField(default=STATUS.DRAFT, choices=STATUS)

    tags = TaggableManager()
    objects = JobManager()

    @transition(field=state, source=STATUS.DRAFT, target=STATUS.ACTIVE)
    def activate(self):
        pass

    @transition(field=state, source='*', target=STATUS.ARCHIVED)
    def archive(self):
        pass

    def __str__(self):
        return f'{self.title} {self.company.name} {self.author.first_name}'
