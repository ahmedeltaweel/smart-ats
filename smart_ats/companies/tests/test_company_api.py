import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from smart_ats.companies.models import Company, CompanyAdmin


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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Elsaeed")
        self.assertEqual(response.data[0]["address"], "Mansoura")
        self.assertEqual(response.data[0]["description"], "Bla Company")
        self.assertEqual(response.data[0]["website"], "http://elsaeed.com")

    def test_company_list_unauthenticated(self):
        client = APIClient()
        response = client.get(self._api_path, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_detail_retreive(self):
        response = self.client.get(
            "{}{}/".format(self._api_path, self.company.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Elsaeed")
        self.assertEqual(response.data["address"], "Mansoura")
        self.assertEqual(response.data["description"], "Bla Company")
        self.assertEqual(response.data["website"], "http://elsaeed.com")

    def test_company_detail_retreive_by_ananymous(self):
        client = APIClient()
        response = client.get(
            "{}{}/".format(self._api_path, self.company.id),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_company_create_by_admin(self):
        data = {
            "name": "DRF",
            "address": "LA",
            "description": "DRF is awesome",
            "website": "http://bla.com",
        }
        response = self.client.post(
            "{}".format(self._api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "DRF")
        self.assertEqual(response.data["address"], "LA")
        self.assertEqual(response.data["description"], "DRF is awesome")
        self.assertEqual(response.data["website"], "http://bla.com")

    def test_company_create_by_ananymous(self):
        data = {
            "name": "LOL",
            "address": "NYC",
            "description": "LOL",
            "website": "http://lol.com",
        }
        client = APIClient()
        response = client.post(
            "{}".format(self._api_path),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

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

    def test_company_update_by_ananymous(self):
        client = APIClient()
        response = client.patch(
            "{}{}/".format(self._api_path, self.company.id),
            data=json.dumps({"name": "Bla", "address": "Bla"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_company_full_update_by_companyadmin(self):
        response = self.client.put(
            "{}{}/".format(self._api_path, self.company.id),
            data=json.dumps(
                {
                    "name": "Django",
                    "address": "Amsterdam",
                    "website": "http://djangoproject.com",
                    "description": "dj project",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["name"], "Django")
        self.assertEqual(response["address"], "Amsterdam")
        self.assertEqual(response["website"], "http://djangoproject.com")
        self.assertEqual(response["description"], "dj project")

    def test_company_full_update_by_ananymous(self):
        client = APIClient()
        response = client.put(
            "{}{}/".format(self._api_path, self.company.id),
            data=json.dumps(
                {
                    "name": "Flask",
                    "address": "Dublin",
                    "website": "http://flask.com",
                    "description": "flask project",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_company_delete_by_companyadmin(self):
        response = self.client.delete("{}{}/".format(self._api_path, self.company.id))
        self.assertEqual(response.status_code, 204)

    def test_company_delete_by_ananymous(self):
        client = APIClient()
        response = client.delete("{}{}/".format(self._api_path, self.company.id))
        self.assertEqual(response.status_code, 403)
