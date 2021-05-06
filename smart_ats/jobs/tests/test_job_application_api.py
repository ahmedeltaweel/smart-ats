import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .factories import JobApplicationFactory, JobFactory


class JobApplicationTest(APITestCase):
    def setUp(self):
        self.job = JobFactory.create(state="ACTIVE")
        self.application = JobApplicationFactory.create(
            job_id=self.job.id, user_id=self.job.author.id
        )
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

    def test_activate_action(self):
        self.application.state = "DRAFT"
        self.application.save()
        response = self.client.patch(
            "{}{}/activate/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shortlisted_action(self):
        self.application.state = "ACTIVE"
        self.application.save()
        response = self.client.patch(
            "{}{}/shortlisted/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejected_action(self):
        self.application.state = "ACTIVE"
        self.application.save()
        response = self.client.patch(
            "{}{}/rejected/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_action(self):
        response = self.client.patch(
            "{}{}/archive/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_action_unauthorized(self):
        response = APIClient().patch(
            "{}{}/archive/".format(self.api_path, self.application.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
