from core.ticket import Ticket
from patterns.behavioral.observer import TicketNotifier


class Command:
    def execute(self) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class AssignTicketCommand(Command):
    def __init__(self, ticket: Ticket, assignee: str, notifier: TicketNotifier):
        # Команда назначения тикета исполнителю.
        self.ticket = ticket
        self.assignee = assignee
        self.notifier = notifier

    def execute(self) -> None:
        self.ticket.assignee = self.assignee
        print(f"[Command] Ticket #{self.ticket.ticket_id} assigned to {self.assignee}.")
        self.notifier.notify(self.ticket, f"Ticket assigned to {self.assignee}.")


class ChangeStatusCommand(Command):
    def __init__(self, ticket: Ticket, new_status: str, notifier: TicketNotifier):
        # Команда ручного изменения статуса тикета.
        self.ticket = ticket
        self.new_status = new_status
        self.notifier = notifier

    def execute(self) -> None:
        old_status = self.ticket.status
        self.ticket.status = self.new_status

        print(
            f"[Command] Ticket #{self.ticket.ticket_id} "
            f"status changed from {old_status} to {self.new_status}."
        )

        self.notifier.notify(
            self.ticket,
            f"Ticket status changed from {old_status} to {self.new_status}."
        )


class CloseTicketCommand(Command):
    def __init__(self, ticket: Ticket, notifier: TicketNotifier):
        # Команда закрытия тикета.
        self.ticket = ticket
        self.notifier = notifier

    def execute(self) -> None:
        self.ticket.status = "Closed"
        print(f"[Command] Ticket #{self.ticket.ticket_id} closed.")
        self.notifier.notify(self.ticket, "Ticket has been closed.")


class CommandInvoker:
    def __init__(self):
        # История выполненных команд.
        self.history: list[Command] = []

    def execute_command(self, command: Command) -> None:
        # Выполняем команду и сохраняем её в истории.
        command.execute()
        self.history.append(command)

    def show_history(self) -> None:
        # Показываем количество выполненных команд.
        print(f"[Command] Executed commands count: {len(self.history)}")