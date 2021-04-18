
from rest_framework.routers import DefaultRouter
from smart_ats.jobs.api import views


router = DefaultRouter()
router.register('job', views.JobViewSet)

urlpatterns = router.urls

