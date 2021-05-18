from .factories import JobApplicationFactory
from django.test import TestCase
from smart_ats.jobs.tasks import cv


class TestCvParserData(TestCase):
    def test_success_extract_data(self):
        job_application = JobApplicationFactory.create()
        self.assertEqual(cv(job_application.cv_url), job_application.data)
