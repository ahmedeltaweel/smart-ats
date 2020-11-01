import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from smart_ats.companies.models import Company, CompanyAdmin

# Create your tests here.


class CompanyAdminTestCase(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Elsaeed",
            website="http://elsaeed.com",
            description="Bla Company",
            address="Mansoura",
        )
        self.company_admin = CompanyAdmin.objects.create(
            username="elsaeed",
            email="elsaeed@email.com",
            password="testpass",
            company=self.company,
        )
        token = Token.objects.get_or_create(user=self.company_admin)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token[0].key)

        self._api_path = "/api/companies/"

    def test_company_list_authenticated(self):
        response = self.client.get("/api/companies/", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_list_un_authenticated(self):
        response = self.client.get(self._api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_detail_retreive(self):
        response = self.client.get(
            "{}1/".format(self._api_path), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Elsaeed")

    def test_company_update_by_companyadmin(self):
        response = self.client.patch(
            "{}{}/".format(self._api_path, self.company.id),
            data=json.dumps({"name": "Hamada", "address": "Cairo"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["name"], "Hamada")
        self.assertEqual(response["address"], "Cairo")
