from .factories import JobApplicationFactory
from django.test import TestCase
from smart_ats.jobs.tasks import cv
from smart_ats.jobs.models import JobApplication


class TestCvParserData(TestCase):
    def test_success_extract_data(self):
        job_application = JobApplicationFactory.create()
        cv("https://www.sec.gov/jobs/sample-resume/sample-resume.pdf", job_application.id)
        self.assertEqual('Address Town', JobApplication.objects.get(id=job_application.id).data['name'])
        self.assertEqual(['MBA - Business Management'],
                         JobApplication.objects.get(id=job_application.id).data['degree'])
        self.assertEqual(4, JobApplication.objects.get(id=job_application.id).data['no_of_pages'])
