
import factory
from factory.django import DjangoModelFactory

from smart_ats.jobs.models import Category, Job
from smart_ats.companies.tests.factories import CompanyFactory, CompanyAdminFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["name"]

    name = factory.Faker("pystr", max_chars=15)


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    description = factory.Faker("catch_phrase")
    category = factory.SubFactory(CategoryFactory)
    company = factory.SubFactory(CompanyFactory)
    author = factory.SubFactory(CompanyAdminFactory)
    state = Job.STATUS.DRAFT
    tags = ','.join([f'{x}_tag' for x in range(3)])
