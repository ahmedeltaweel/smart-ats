from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompaniesConfig(AppConfig):
    name = "smart_ats.companies"
    verbose_name = _("Companies")
