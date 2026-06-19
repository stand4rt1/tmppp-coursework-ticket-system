from core.ticket import Ticket


class TicketState:
    def next_state(self, ticket: Ticket) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class NewState(TicketState):
    def next_state(self, ticket: Ticket) -> None:
        # Новый тикет переходит в обработку.
        ticket.status = "In Progress"
        print(f"[State] Ticket #{ticket.ticket_id} moved to In Progress.")


class InProgressState(TicketState):
    def next_state(self, ticket: Ticket) -> None:
        # Тикет в обработке переходит в решённый.
        ticket.status = "Resolved"
        print(f"[State] Ticket #{ticket.ticket_id} moved to Resolved.")


class ResolvedState(TicketState):
    def next_state(self, ticket: Ticket) -> None:
        # Решённый тикет закрывается.
        ticket.status = "Closed"
        print(f"[State] Ticket #{ticket.ticket_id} moved to Closed.")


class ClosedState(TicketState):
    def next_state(self, ticket: Ticket) -> None:
        # Закрытый тикет дальше не переводится.
        print(f"[State] Ticket #{ticket.ticket_id} is already Closed.")


class TicketStateContext:
    def move_next(self, ticket: Ticket) -> None:
        # Контекст выбирает нужное состояние на основе текущего статуса тикета.
        if ticket.status == "New":
            NewState().next_state(ticket)
        elif ticket.status == "In Progress":
            InProgressState().next_state(ticket)
        elif ticket.status == "Resolved":
            ResolvedState().next_state(ticket)
        else:
            ClosedState().next_state(ticket)