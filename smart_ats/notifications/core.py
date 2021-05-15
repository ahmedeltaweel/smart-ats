from django.core.mail import send_mail


class SmsNotification:
    @staticmethod
    def send(data: str):
        # call sms service call twilio.
        print("========SMS===========")
        print(data)


class EmailNotification:
    @staticmethod
    def send(data: str, email: str) -> None:
        # call sms service call sendgrid
        send_mail(
            subject="no-reply",
            message=data,
            html_message=data,
            recipient_list=[email],
            from_email="no-reply@taher.com",
        )
