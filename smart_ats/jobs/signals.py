from django.dispatch import Signal, receiver

from .celery_tasks import notify_comapnyadmin

JobApplicationActivatedSignal = Signal()


@receiver(
    JobApplicationActivatedSignal,
)
def job_activated(sender, instance, *args, **kwargs):
    notify_comapnyadmin.apply_async(
        args=(instance.id, instance.job.company.id),
    )
