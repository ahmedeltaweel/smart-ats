from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationConfig(AppConfig):
    name = "smart_ats.notifications"
    verbose_name = _("Notifications")
