from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class User(AbstractUser):
    """Default user for Smart ATS."""

    STATUSES = Choices(
        (
            "admin",
            _("Admin"),
        ),
        ("candidate", _("Candidate")),
    )

    user_type = models.CharField(
        choices=STATUSES, default=STATUSES.candidate, max_length=15
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
