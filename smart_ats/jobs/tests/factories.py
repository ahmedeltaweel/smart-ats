import factory
from factory.django import DjangoModelFactory

from smart_ats.companies.tests.factories import CompanyAdminFactory, CompanyFactory
from smart_ats.jobs.models import Category, Job, JobApplication
from smart_ats.users.tests.factories import UserFactory


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
    author = factory.SubFactory(
        CompanyAdminFactory, company=factory.SelfAttribute("..company")
    )
    state = Job.STATUS.DRAFT
    tags = ",".join([f"{x}_tag" for x in range(3)])


class JobApplicationFactory(DjangoModelFactory):
    class Meta:
        model = JobApplication

    user = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)
    state = JobApplication.STATUS.DRAFT
    data = {
        "name": "Hamada",
        "adress": "Hamada Second Floor",
        "skills": ["python", "django", "postgres", "docker"],
    }
    cv_url = factory.Faker("url")
