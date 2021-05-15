from .tasks import notify_comapnyadmin


def job_activated(instance) -> None:
    notify_comapnyadmin.apply_async(
        args=(instance.id, instance.job.title, instance.job.company.id),
    )
