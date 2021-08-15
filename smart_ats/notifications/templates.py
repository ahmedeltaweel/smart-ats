from enum import Enum


class EmailTemplates(Enum):
    BASE = "notifications/email/base.html"
    JOBAPPLY = "notifications/email/job_apply.html"


class SMSTemplates(Enum):
    BASE = "notifications/sms/base.txt"
