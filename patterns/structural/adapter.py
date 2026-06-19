from services.notification_service import ExternalMessengerAPI


class NotificationSender:
    def send(self, recipient: str, message: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class MessengerNotificationAdapter(NotificationSender):
    def __init__(self, external_api: ExternalMessengerAPI):
        # Адаптер хранит внешний API, у которого несовместимый интерфейс.
        self.external_api = external_api

    def send(self, recipient: str, message: str) -> None:
        # Приводим метод push_message() к общему интерфейсу send().
        self.external_api.push_message(recipient, message)