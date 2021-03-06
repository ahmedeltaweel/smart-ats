from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from smart_ats.jobs.api.views import JobViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r"companies/(?P<company_id>\d+)/jobs", JobViewSet, "jobs")

app_name = "jobs"
urlpatterns = router.urls
