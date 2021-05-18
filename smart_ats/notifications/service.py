from dataclasses import dataclass
from typing import Any, Dict, List, Union

from django.conf import settings
from django.template.loader import render_to_string

from .exceptions import (
    UnSupportedNotificationContextException,
    UnSupportedNotificationMethodException,
)
from .templates import EmailTemplates, SMSTemplates


@dataclass
class EmailContent:
    message: str
    html_message: str
    recipient_list: List[str]
    subject: str
    from_email: str = settings.DEFAULT_FROM_EMAIL


@dataclass(frozen=True)
class NotificationContent:
    context: Dict[str, Any]
    template: Union[EmailTemplates, SMSTemplates]


class NotificationContentConstructorService:
    def __init__(self, content: NotificationContent):
        self.content = content

    def _validate(self) -> None:
        if (
            self.content.template not in SMSTemplates
            and self.content.template not in EmailTemplates
        ):
            raise UnSupportedNotificationMethodException(
                f"you can not send notification using {self.content.template.__class__}"
            )
        if "receiver_name" not in self.content.context.keys():
            raise UnSupportedNotificationContextException(
                f"you can not send notification using {self.content.context}"
            )

    def construct_notification(self) -> str:
        self._validate()
        return render_to_string(self.content.template.value, self.content.context)
