from django.test import TestCase

from smart_ats.jobs.models import JobApplication
from smart_ats.jobs.tests.factories import JobApplicationFactory


class JobApplicationTest(TestCase):
    def test_created_job_application(self):
        JobApplicationFactory.create()
        self.assertEqual(JobApplication.objects.count(), 1)
