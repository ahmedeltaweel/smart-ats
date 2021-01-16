from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from django.template.loader import render_to_string

from .exceptions import (
    UnSupportedNotificationContextException,
    UnSupportedNotificationMethodException,
)


class Methods(Enum):
    sms = "txt"
    email = "html"


@dataclass(frozen=True)
class NotificationContent:
    context: Dict["str", Any]
    template_name: str
    method: str


class NotificationContentConstructorService:
    def __init__(self, content: NotificationContent):
        self.content = content

    def _validate(self) -> None:
        if self.content.method not in Methods:
            raise UnSupportedNotificationMethodException(
                f"you can not send notification using {self.content.method}"
            )
        if "receiver_name" not in self.content.context.keys():
            raise UnSupportedNotificationContextException(
                f"you can not send notification using {self.content.context}"
            )

    def construct_notification(self) -> (str, str):
        self._validate()
        return (
            render_to_string(
                f"notifications/{self.content.method.name}/base.{self.content.method.value}",
                self.content.context,
            ),
            self.content.method,
        )
