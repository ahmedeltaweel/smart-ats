import factory
import factory.fuzzy
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


job_application_status_list = [s[0] for s in JobApplication.STATUS]


class JobApplicationFactory(DjangoModelFactory):
    class Meta:
        model = JobApplication

    user = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)
    state = factory.fuzzy.FuzzyChoice(job_application_status_list)
    data = factory.Dict(
        {
            "name": factory.Faker("name"),
            "adress": factory.Faker("address"),
            "LinkedIn": factory.Faker("url"),
        }
    )
    cv_url = factory.Faker("url")
