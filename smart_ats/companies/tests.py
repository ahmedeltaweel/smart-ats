from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

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
        self.token = Token.objects.create(user=self.company_admin)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_company_list_authenticated(self):
        response = self.client.get("/api/companies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/companies/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_detail_retreive(self):
        response = self.client.get("/api/companies/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Elsaeed")

    # def test_company_update_by_companyadmin(self):
    # 	response = self.client.put('/api/companies/1/',{"name":"Hamada","address":"Cairo"})
    # 	self.assertEqual(response.status_code, status.HTTP_200_OK)
    # 	self.assertEqual(json.loads(response.content),{"id":1,"company_admin":"elsaeed","name":"Hamada",
    # 												"website":"http://elsaeed.com","address":"Cairo"})
