import factory
from factory.django import DjangoModelFactory

from smart_ats.companies.models import Company, CompanyAdmin
from smart_ats.users.models import User
from smart_ats.users.tests.factories import UserFactory


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company
        django_get_or_create = ["name"]

    name = factory.Faker("pystr", max_chars=15)
    description = factory.Faker("catch_phrase")
    website = factory.Faker("url")
    address = factory.Faker("address")
    is_active = factory.Faker("pybool")


class CompanyAdminFactory(UserFactory):
    company = factory.SubFactory(CompanyFactory)
    user_type = User.STATUSES.admin

    class Meta:
        model = CompanyAdmin
        django_get_or_create = ["username"]
