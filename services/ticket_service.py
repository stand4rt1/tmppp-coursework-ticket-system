from core.ticket import Ticket


class TicketService:
    def __init__(self):
        # Список используется как простое временное хранилище тикетов.
        self._tickets: list[Ticket] = []
        self._next_id = 1

    def get_next_id(self) -> int:
        # Генерируем новый уникальный номер тикета.
        ticket_id = self._next_id
        self._next_id += 1
        return ticket_id

    def save_ticket(self, ticket: Ticket) -> Ticket:
        # Сохраняем тикет в системе.
        self._tickets.append(ticket)
        print(f"[Ticket Service] Ticket #{ticket.ticket_id} saved.")
        return ticket

    def get_ticket_by_id(self, ticket_id: int) -> Ticket | None:
        # Ищем тикет по его идентификатору.
        for ticket in self._tickets:
            if ticket.ticket_id == ticket_id:
                return ticket

        return None

    def get_all_tickets(self) -> list[Ticket]:
        # Возвращаем все созданные тикеты.
        return self._tickets