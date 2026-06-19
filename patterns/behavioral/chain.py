from core.ticket import Ticket


class TicketHandler:
    def __init__(self):
        # Следующий обработчик в цепочке.
        self.next_handler = None

    def set_next(self, handler):
        # Связываем текущий обработчик со следующим.
        self.next_handler = handler
        return handler

    def handle(self, ticket: Ticket) -> None:
        # Если следующий обработчик существует, передаём тикет дальше.
        if self.next_handler:
            self.next_handler.handle(ticket)


class CategoryValidationHandler(TicketHandler):
    def handle(self, ticket: Ticket) -> None:
        # Проверяем, что у тикета указана категория.
        if not ticket.category:
            print(f"[Chain] Ticket #{ticket.ticket_id} has no category.")
            return

        print(f"[Chain] Category validated for ticket #{ticket.ticket_id}.")
        super().handle(ticket)


class PriorityValidationHandler(TicketHandler):
    def handle(self, ticket: Ticket) -> None:
        # Проверяем, что приоритет уже рассчитан.
        if ticket.priority == "Undefined":
            print(f"[Chain] Ticket #{ticket.ticket_id} has undefined priority.")
            return

        print(f"[Chain] Priority validated for ticket #{ticket.ticket_id}.")
        super().handle(ticket)


class AssignmentHandler(TicketHandler):
    def handle(self, ticket: Ticket) -> None:
        # Назначаем исполнителя в зависимости от приоритета.
        if ticket.priority == "High":
            ticket.assignee = "Senior Support Specialist"
        elif ticket.priority == "Medium":
            ticket.assignee = "Support Specialist"
        else:
            ticket.assignee = "Junior Support Specialist"

        print(f"[Chain] Ticket #{ticket.ticket_id} assigned to {ticket.assignee}.")
        super().handle(ticket)


class FinalProcessingHandler(TicketHandler):
    def handle(self, ticket: Ticket) -> None:
        # Завершающий обработчик фиксирует успешную обработку.
        print(f"[Chain] Ticket #{ticket.ticket_id} successfully processed.")


def build_ticket_processing_chain() -> TicketHandler:
    # Создаём цепочку обработки тикета.
    category_handler = CategoryValidationHandler()
    priority_handler = PriorityValidationHandler()
    assignment_handler = AssignmentHandler()
    final_handler = FinalProcessingHandler()

    category_handler.set_next(priority_handler).set_next(assignment_handler).set_next(final_handler)

    return category_handler