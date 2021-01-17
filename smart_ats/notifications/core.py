class SmsNotification:
    @staticmethod
    def send(data: str):
        # call sms service call twilio.
        print("========SMS===========")
        print(data)


class EmailNotification:
    @staticmethod
    def send(data: str):
        # call sms service call sendgrid
        print("=======EMAIL============")
        print(data)
