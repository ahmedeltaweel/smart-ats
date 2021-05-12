from config.celery_app import app
from smart_ats.companies.models import CompanyAdmin


@app.task
def notify_comapnyadmin(instance_id, company_id):
    company_admins = CompanyAdmin.objects.filter(company_id=company_id)
    for company_admin in company_admins:
        print(
            f"dear {company_admin.username} job Application {instance_id} is activated for job "
        )
