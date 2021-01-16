from typing import Protocol


class NotificationInterface(Protocol):
    def send(self, data: str) -> None:
        raise NotImplementedError()


class SmsNotification:
    @staticmethod
    def send(data: str):
        # call sms service call twilio.
        print("===================")
        print(data)


class EmailNotification:
    @staticmethod
    def send(data: str):
        # call sms service call sendgrid
        print("===================")
        print(data)
