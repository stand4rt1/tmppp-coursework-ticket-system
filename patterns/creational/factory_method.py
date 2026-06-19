from services.notification_service import (
    EmailNotificationService,
    SmsNotificationService,
    ExternalMessengerAPI
)


class Notification:
    def send(self, recipient: str, message: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class EmailNotification(Notification):
    def __init__(self):
        self.service = EmailNotificationService()

    def send(self, recipient: str, message: str) -> None:
        # Конкретная реализация email-уведомления.
        self.service.send_email(recipient, message)


class SmsNotification(Notification):
    def __init__(self):
        self.service = SmsNotificationService()

    def send(self, recipient: str, message: str) -> None:
        # В учебной версии recipient используется как номер телефона.
        self.service.send_sms(recipient, message)


class MessengerNotification(Notification):
    def __init__(self):
        self.service = ExternalMessengerAPI()

    def send(self, recipient: str, message: str) -> None:
        # Внешний messenger API имеет свой способ отправки сообщения.
        self.service.push_message(recipient, message)


class NotificationFactory:
    def create_notification(self, notification_type: str) -> Notification:
        # Factory Method выбирает нужный объект уведомления по типу.
        notification_type = notification_type.lower()

        if notification_type == "email":
            return EmailNotification()

        if notification_type == "sms":
            return SmsNotification()

        if notification_type == "messenger":
            return MessengerNotification()

        raise ValueError(f"Unknown notification type: {notification_type}")