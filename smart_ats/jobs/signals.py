from django.dispatch import Signal, receiver

JobApplicationActivatedSignal = Signal()


@receiver(
    JobApplicationActivatedSignal,
)
def notify_comapnyadmin(sender, instance, **kwargs):
    company_admins = instance.job.company.company_admin.all()
    for company_admin in company_admins:
        print(
            f"dear {company_admin.username} job Application {instance} is activated for job "
        )
