import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from smart_ats.companies.tests.factories import CompanyAdminFactory

from .factories import CategoryFactory, JobApplicationFactory, JobFactory

User = get_user_model()


class JobAPITestCase(APITestCase):
    def setUp(self):
        self.job = JobFactory.create()
        token = Token.objects.get_or_create(user=self.job.author)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)
        self.api_path = f"/api/v1/companies/{self.job.company_id}/jobs/"

    def test_company_list_unauthenticated(self):
        client = APIClient()
        response = client.get(self.api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_list_data_authenticated(self):
        response = self.client.get(f"{self.api_path}", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], self.job.title)
        self.assertEqual(response.data[0]["description"], self.job.description)
        self.assertEqual(response.data[0]["category"]["id"], self.job.category.id)
        self.assertEqual(response.data[0]["state"], self.job.state)

    def test_delete_job_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_job_company_admin(self):
        response = self.client.delete(
            f"{self.api_path}{self.job.id}/", content_type="application/json"
        )
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
        self.assertEqual(response.data["category"]["id"], self.job.category.id)
        self.assertEqual(response.data["state"], self.job.state)

    def test_job_detail_retreive_by_ananymous(self):
        client = APIClient()
        response = client.get(
            "{}{}/".format(self.api_path, self.job.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_job_create_by_admin(self):
        category = CategoryFactory.create()
        data = {
            "title": "title1",
            "description": "temp",
            "category": category.id,
            "company": self.job.company_id,
            "state": "DRAFT",
            "tags": ["tag1", "tag2"],
        }
        response = self.client.post(
            "{}".format(self.api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "title1")
        self.assertEqual(response.data["description"], "temp")
        self.assertEqual(response.data["category"], category.id)
        self.assertEqual(response.data["company"], self.job.company.id)
        self.assertEqual(response.data["author"], self.job.author.id)
        self.assertEqual(response.data["state"], "DRAFT")
        self.assertCountEqual(response.data["tags"], ["tag1", "tag2"])

    def test_job_create_by_ananymous(self):
        data = {
            "title": "no title",
            "description": "no temp",
            "category": "",
            "company": "LOL",
            "author": self.job.author.id,
            "state": "DRAFT",
            "tags": ["tag1", "tag2"],
        }
        client = APIClient()
        response = client.post(
            "{}".format(self.api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_job_update_by_admin(self):
        data = {"title": "updated title"}

        response = self.client.patch(
            f"{self.api_path}{self.job.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])

    def test_job_update_by_ananumous(self):
        data = {"title": "updated title"}

        client = APIClient()
        response = client.patch(
            f"{self.api_path}{self.job.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_update_by_another_company_admin(self):
        admin = CompanyAdminFactory.create()
        token = Token.objects.get_or_create(user=admin)
        client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)
        data = {"title": "updated title"}

        response = client.patch(
            f"{self.api_path}{self.job.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_update_by_another_admin_same_company(self):
        admin_2 = CompanyAdminFactory()
        admin_2.company_id = self.job.company_id
        admin_2.save()

        token = Token.objects.get_or_create(user=admin_2)
        client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)

        data = {"title": "updated title"}

        response = client.patch(
            f"{self.api_path}{self.job.id}/",
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])

    def test_activate_state_admin(self):
        response = self.client.patch(
            f"{self.api_path}{self.job.id}/activate/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Ok")

    def test_activate_state_ananymous(self):
        client = APIClient()
        response = client.patch(
            f"{self.api_path}{self.job.id}/activate/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_archive_state_admin(self):
        response = self.client.patch(
            f"{self.api_path}{self.job.id}/archive/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Ok")

    def test_archive_state_ananymous(self):
        client = APIClient()
        response = client.patch(
            f"{self.api_path}{self.job.id}/archive/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_create_by_admin_with_no_title(self):
        category = CategoryFactory.create()
        data = {
            "description": "temp",
            "category": category.id,
            "company": self.job.company_id,
            "author": self.job.author.id,
            "state": "DRAFT",
            "tags": ["tag1", "tag2"],
        }
        response = self.client.post(
            "{}".format(self.api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_with_DoesNotExist_company_id(self):
        response = self.client.get(
            "/api/v1/companies/-1/jobs/", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobApplicationTest(APITestCase):
    def setUp(self):
        self.job = JobFactory()
        self.job.state = "ACTIVE"
        self.job.save()
        self.application = JobApplicationFactory()
        self.application.job_id = self.job.id
        self.application.user_id = self.job.author.id
        self.application.save()
        token = Token.objects.get_or_create(user=self.job.author)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)
        self.api_path = f"/api/v1/jobs/{self.job.id}/apply/"

    def test_apply_for_job(self):
        data = {"data": self.application.data, "cv_url": self.application.cv_url}
        response = self.client.post(
            "{}".format(self.api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.job.author.id)
        self.assertEqual(response.data["job"], self.job.id)
        self.assertEqual(response.data["state"], "DRAFT")
        self.assertEqual(response.data["cv_url"], self.application.cv_url)
        self.assertEqual(response.data["data"], self.application.data)

    def test_list_job_applications_authorized(self):
        response = self.client.get(
            "{}".format(self.api_path),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["user"]["id"], self.job.author.id)
        self.assertEqual(response.data[0]["job"]["id"], self.job.id)
        self.assertEqual(response.data[0]["state"], self.application.state)
        self.assertEqual(response.data[0]["cv_url"], self.application.cv_url)
        self.assertEqual(response.data[0]["data"], self.application.data)

    def test_list_job_applications_unauthorized(self):
        response = APIClient().get(
            "{}".format(self.api_path),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_apply_for_non_Active_job(self):
        non_Active_job = JobFactory.create()
        data = {"data": self.application.data, "cv_url": self.application.cv_url}
        response = self.client.post(
            f"/api/v1/jobs/{non_Active_job.id}/apply/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_apply_for_job_with_no_cv_url(self):
        data = {
            "data": self.application.data,
        }
        response = self.client.post(
            "{}".format(self.api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retirieve_application(self):
        response = self.client.get(
            "{}{}/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["id"], self.job.author.id)
        self.assertEqual(response.data["job"]["id"], self.job.id)
        self.assertEqual(response.data["state"], self.application.state)
        self.assertEqual(response.data["cv_url"], self.application.cv_url)
        self.assertEqual(response.data["data"], self.application.data)
