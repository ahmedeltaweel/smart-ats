from .factories import JobApplicationFactory
from django.test import TestCase
from smart_ats.jobs.tasks import cv
from smart_ats.jobs.models import JobApplication
from unittest.mock import patch


class TestCvParserData(TestCase):
    @patch("smart_ats.jobs.models.cv.delay")
    def test_saving_data_after_activation(self, mocked_func):
        job_application = \
            JobApplicationFactory.create(state="DRAFT",
                                         cv_url="https://www.sec.gov/jobs/sample-resume/sample-resume.pdf")
        job_application.activate()
        self.assertEqual(mocked_func.called, True)
        mocked_func.assert_called_with(job_application.cv_url, job_application.id)

    def test_success_extract_data(self):
        job_application = JobApplicationFactory.create()
        cv("https://www.sec.gov/jobs/sample-resume/sample-resume.pdf", job_application.id)
        self.assertEqual('Address Town', JobApplication.objects.get(id=job_application.id).data['name'])
        self.assertEqual(['MBA - Business Management'],
                         JobApplication.objects.get(id=job_application.id).data['degree'])
        self.assertEqual(4, JobApplication.objects.get(id=job_application.id).data['no_of_pages'])
