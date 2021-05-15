from django.core import mail
from django.test.testcases import TestCase

from smart_ats.companies.models import CompanyAdmin
from smart_ats.jobs.tasks import notify_comapnyadmin

from .factories import JobApplicationFactory


class TestSentmailAfterApply(TestCase):
    def test_success_to_notify_admins(self):
        job_apply = JobApplicationFactory.create(state="DRAFT")
        notify_comapnyadmin(job_apply.id, job_apply.job.title, job_apply.job.company_id)
        company_admins = [
            c.email
            for c in CompanyAdmin.objects.filter(company_id=job_apply.job.company_id)
        ]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "no-reply")
        self.assertListEqual(mail.outbox[0].to, company_admins)
