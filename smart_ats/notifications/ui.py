from django.http import HttpResponse

from .core import EmailNotification, SmsNotification
from .service import NotificationContent, NotificationContentConstructorService
from .templates import EmailTemplates, SMSTemplates


class Notification:
    def __init__(self, content: NotificationContent):
        self.content = NotificationContentConstructorService(
            content
        ).construct_notification()

    def sms(self) -> None:
        SmsNotification.send(self.content)

    def email(self) -> None:
        EmailNotification.send(self.content)


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
