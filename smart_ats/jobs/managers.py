from django.db import models


class JobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("company", "author")


class JobApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("job", "user")
