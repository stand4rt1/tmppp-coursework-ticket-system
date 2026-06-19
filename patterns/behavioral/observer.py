from core.ticket import Ticket


class Observer:
    def update(self, ticket: Ticket, message: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class EmailObserver(Observer):
    def update(self, ticket: Ticket, message: str) -> None:
        # Имитация уведомления владельца тикета по email.
        print(f"[Observer: Email] Ticket #{ticket.ticket_id}: {message}")


class ManagerObserver(Observer):
    def update(self, ticket: Ticket, message: str) -> None:
        # Имитация уведомления менеджера поддержки.
        print(f"[Observer: Manager] Ticket #{ticket.ticket_id}: {message}")


class AuditObserver(Observer):
    def update(self, ticket: Ticket, message: str) -> None:
        # Имитация записи события в журнал аудита.
        print(f"[Observer: Audit] Ticket #{ticket.ticket_id}: {message}")


class TicketNotifier:
    def __init__(self):
        # Список объектов, которые должны получать уведомления.
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        # Добавляем нового подписчика.
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        # Удаляем подписчика.
        self._observers.remove(observer)

    def notify(self, ticket: Ticket, message: str) -> None:
        # Отправляем сообщение всем подписчикам.
        for observer in self._observers:
            observer.update(ticket, message)