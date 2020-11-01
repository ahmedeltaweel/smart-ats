from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from smart_ats.companies.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("companies", views.CompanyViewSet, "companies")

app_name = "companies"
urlpatterns = router.urls
