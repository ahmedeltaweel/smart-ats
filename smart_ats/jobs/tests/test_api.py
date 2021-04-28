from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from .factories import JobFactory
from smart_ats.companies.tests.factories import CompanyFactory

User = get_user_model()


class JobAPITestCase(APITestCase):
    def setUp(self):
        self.job = JobFactory.create()
        token = Token.objects.get_or_create(user=self.job.author)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)
        self.api_path = "/api/jobs/"

    def test_jobs_list_authenticated(self):
        response = self.client.get(f"{self.api_path}", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_company_list_unauthenticated(self):
        client = APIClient()
        response = client.get(self.api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_list_data(self):
        response = self.client.get(f"{self.api_path}", content_type="application/json")
        self.assertEqual(response.data[0]["title"], self.job.title)
        self.assertEqual(response.data[0]["description"], self.job.description)
        self.assertEqual(response.data[0]["category"], f"{self.job.category}")
        self.assertEqual(response.data[0]["state"], self.job.state)

    def test_delete_job_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_job_company_admin(self):
        response = self.client.delete(f"{self.api_path}", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_job_normal_user(self):
        user = User.objects.create_user(
            username="hamada", email="hamada@mail.com", password="hamadapass"
        )
        token = Token.objects.get_or_create(user=user)
        user = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)
        response = user.delete(f"{self.api_path}", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_detail_retreive(self):
        response = self.client.get(
            "{}{}/".format(self.api_path, self.job.id),
            content_type="application/json",
        )
        self.assertEqual(response.data["title"], self.job.title)
        self.assertEqual(response.data["description"], self.job.description)
        self.assertEqual(response.data["category"], f"{self.job.category}")
        self.assertEqual(response.data["state"], self.job.state)

    def test_job_detail_retreive_by_ananymous(self):
        client = APIClient()
        response = client.get(
            "{}{}/".format(self._api_path, self.job.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_job_create_by_admin(self):
        category = CategoryFactory.create()
        data = {
            "title": "title1",
            "description": "temp",
            "category": category.id,
            "company": self.job.company.id,
            "author": "name",
            "state": "DRAFT",
            "tags": "",
        }
        response = self.client.post(
            "{}".format(self._api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "title1")
        self.assertEqual(response.data["description"], "temp")
        self.assertEqual(response.data["category"], category.id)
        self.assertEqual(response.data["company"], self.job.company.id)
        self.assertEqual(response.data["author"], "name")
        self.assertEqual(response.data["state"], "DRAFT")
        self.assertEqual(response.data["tags"], "")

    def test_company_create_by_ananymous(self):
        data = {
            "title": "no title",
            "description": "no temp",
            "category": "",
            "company": "LOL",
            "author": "anan",
            "state": "DRAFT",
            "tags": "",
        }
        client = APIClient()
        response = client.post(
            "{}".format(self._api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

            



