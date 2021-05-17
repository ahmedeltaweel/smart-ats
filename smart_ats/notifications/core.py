from django.core.mail import send_mail

from .service import EmailContent


class SmsNotification:
    @staticmethod
    def send(data: str):
        # call sms service call twilio.
        print("========SMS===========")
        print(data)


class EmailNotification:
    @staticmethod
    def send(mail_data: EmailContent) -> None:
        # call sms service call sendgrid
        send_mail(
            subject=mail_data.subject,
            message=mail_data.message,
            html_message=mail_data.html_message,
            recipient_list=mail_data.recipient_list,
            from_email=mail_data.from_email,
        )
