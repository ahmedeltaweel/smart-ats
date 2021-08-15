from unittest.mock import patch

from django.core import mail
from django.test.testcases import TestCase

from smart_ats.companies.models import CompanyAdmin
from smart_ats.jobs.tasks import notify_comapnyadmin

from .factories import JobApplicationFactory


class TestSentmailAfterApply(TestCase):
    @patch("smart_ats.jobs.models.notify_comapnyadmin.apply_async")
    def test_notifyadmins_After_apply(self, mocked_func):
        job_apply = JobApplicationFactory.create(state="DRAFT")
        job_apply.activate()
        self.assertEqual(mocked_func.called, True)
        mocked_func.assert_called_with(
            args=(job_apply.id, job_apply.job.title, job_apply.job.company_id)
        )

    def test_email_is_sent_for_admins(self):
        job_apply = JobApplicationFactory.create(state="DRAFT")
        notify_comapnyadmin(job_apply.id, job_apply.job.title, job_apply.job.company_id)
        company_admins = [
            c.email
            for c in CompanyAdmin.objects.filter(company_id=job_apply.job.company_id)
        ]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "no-reply")
        self.assertListEqual(mail.outbox[0].to, company_admins)
