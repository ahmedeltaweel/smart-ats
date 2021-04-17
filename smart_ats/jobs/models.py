from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from smart_ats.companies.models import Company, CompanyAdmin
from taggit.managers import TaggableManager

from .managers import JobManager

from django_fsm import FSMField, transition


class Category(TimeStampedModel):
    name = models.CharField(max_length=30, db_index=True)


STATUS = ('Active', 'Draft', 'Archived')
STATUS = list(zip(STATUS, STATUS))
class Job(TimeStampedModel):

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(CompanyAdmin, on_delete=models.CASCADE)
    tags = TaggableManager()

    objects = JobManager()
    state = FSMField(default=STATUS[1], choices=STATUS)

    @transition(field=state, source='Draft', target='Active')
    def start(self):

        pass
    @transition(field=state, source='Active', target='Archived')
    def start(self):

        pass


    def __str__(self):
        return f'{self.title} {self.company.name} {self.author.first_name}'
