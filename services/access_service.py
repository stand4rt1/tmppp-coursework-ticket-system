from core.user import User
from core.ticket import Ticket


class AccessService:
    def can_view_ticket(self, user: User, ticket: Ticket) -> bool:
        # Смотреть тикет может администратор или владелец тикета.
        return user.is_admin() or user.username == ticket.owner

    def can_close_ticket(self, user: User, ticket: Ticket) -> bool:
        # Закрыть тикет может администратор или назначенный исполнитель.
        return user.is_admin() or user.username == ticket.assignee