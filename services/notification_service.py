class EmailNotificationService:
    def send_email(self, recipient: str, message: str) -> None:
        # Базовый сервис отправки email-уведомлений.
        print(f"[Email Service] Email sent to {recipient}: {message}")


class SmsNotificationService:
    def send_sms(self, phone_number: str, message: str) -> None:
        # Базовый сервис отправки SMS.
        print(f"[SMS Service] SMS sent to {phone_number}: {message}")


class ExternalMessengerAPI:
    def push_message(self, user_login: str, text: str) -> None:
        # Имитация внешнего API мессенджера.
        # У него другой интерфейс, поэтому позже подключим его через Adapter.
        print(f"[External Messenger API] Message pushed to {user_login}: {text}")