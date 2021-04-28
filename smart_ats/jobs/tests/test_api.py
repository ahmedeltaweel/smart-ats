from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from .factories import JobFactory

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
