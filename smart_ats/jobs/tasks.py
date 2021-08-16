from config.celery_app import app
from smart_ats.companies.models import CompanyAdmin
from smart_ats.notifications.ui import EmailTemplates, Notification, NotificationContent


@app.task
def notify_comapnyadmin(instance_id, job_name, company_id) -> None:
    company_admins = CompanyAdmin.objects.filter(company_id=company_id)
    for company_admin in company_admins:
        Notification(
            NotificationContent(
                context={
                    "receiver_name": company_admin.username,
                    "job_name": job_name,
                },
                template=EmailTemplates.JOBAPPLY,
            )
        ).email([company_admin.email], subject="A new applicant")
