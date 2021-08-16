from typing import List

from django.http import HttpResponse

from .core import EmailNotification, SmsNotification
from .service import (
    EmailContent,
    NotificationContent,
    NotificationContentConstructorService,
)
from .templates import EmailTemplates


class Notification:
    def __init__(self, content: NotificationContent):
        self.content = NotificationContentConstructorService(
            content
        ).construct_notification()

    def sms(self) -> None:
        SmsNotification.send(self.content)

    def email(self, emails: List[str], subject: str) -> None:
        EmailNotification.send(
            EmailContent(
                message=self.content,
                html_message=self.content,
                recipient_list=emails,
                subject=subject,
            )
        )


def send_notification(request, username: str) -> HttpResponse:
    Notification(
        NotificationContent(
            context={"receiver_name": username},
            template=EmailTemplates.BASE,
        )
    ).email()
    return HttpResponse("notification is sent")


"""
Notification(NotificationContent).sms()
Notification(NotificationContent).email()
"""
