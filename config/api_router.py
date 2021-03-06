from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from smart_ats.companies.api_urls import router as company_router
from smart_ats.jobs.api_urls import router as job_router
from smart_ats.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.registry.extend(company_router.registry)
router.registry.extend(job_router.registry)

app_name = "api"
urlpatterns = router.urls
