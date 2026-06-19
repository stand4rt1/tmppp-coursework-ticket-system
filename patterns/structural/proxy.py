from core.user import User
from core.ticket import Ticket
from services.access_service import AccessService


class TicketAccess:
    def show_ticket(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class RealTicketAccess(TicketAccess):
    def __init__(self, ticket_view):
        # Реальный объект отвечает только за показ тикета.
        self.ticket_view = ticket_view

    def show_ticket(self) -> None:
        print(self.ticket_view.get_info())


class TicketAccessProxy(TicketAccess):
    def __init__(self, user: User, ticket: Ticket, ticket_view, access_service: AccessService):
        # Proxy получает пользователя, тикет и сервис проверки прав.
        self.user = user
        self.ticket = ticket
        self.real_access = RealTicketAccess(ticket_view)
        self.access_service = access_service

    def show_ticket(self) -> None:
        # Перед показом тикета проверяем права доступа.
        if self.access_service.can_view_ticket(self.user, self.ticket):
            print(f"[Proxy] Access granted for user: {self.user.username}")
            self.real_access.show_ticket()
        else:
            print(f"[Proxy] Access denied for user: {self.user.username}")