from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from smart_ats.companies.api.views import CompanyViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("companies", CompanyViewSet)


urlpatterns = router.urls
