from enum import Enum


class EmailTemplates(Enum):
    BASE = "notifications/email/base.html"


class SMSTemplates(Enum):
    BASE = "notifications/sms/base.txt"
