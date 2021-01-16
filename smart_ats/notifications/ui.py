from django.http import HttpResponse

from .core import EmailNotification, SmsNotification
from .service import Methods, NotificationContent, NotificationContentConstructorService


class Notification:
    def __init__(self, content: NotificationContent):
        self.content, self.method = NotificationContentConstructorService(
            content
        ).construct_notification()

    def _sms(self) -> None:
        SmsNotification.send(self.content)

    def _email(self) -> None:
        EmailNotification.send(self.content)

    def notify(self) -> None:
        if self.method == Methods.sms:
            self._sms()
        elif self.method == Methods.email:
            self._email()


def send_notification(request, username: str) -> HttpResponse:
    Notification(
        NotificationContent(
            context={"receiver_name": username},
            template_name="base",
            method=Methods.sms,
        )
    ).notify()
    return HttpResponse("notification is sent")


"""
Notification(NotificationContent).sms()
Notification(NotificationContent).email()
"""
