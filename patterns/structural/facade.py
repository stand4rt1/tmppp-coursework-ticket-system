from core.user import User
from core.ticket import Ticket
from services.ticket_service import TicketService
from services.access_service import AccessService

from patterns.creational.builder import TicketBuilder, TicketDirector
from patterns.creational.factory_method import NotificationFactory

from patterns.structural.decorator import (
    BaseTicketView,
    UrgentTicketViewDecorator,
    SlaTicketViewDecorator,
    ConfidentialTicketViewDecorator
)
from patterns.structural.proxy import TicketAccessProxy
from patterns.structural.composite import build_default_category_tree

from patterns.behavioral.strategy import PriorityContext, CategoryPriorityStrategy, KeywordPriorityStrategy
from patterns.behavioral.observer import TicketNotifier, EmailObserver, ManagerObserver, AuditObserver
from patterns.behavioral.state import TicketStateContext
from patterns.behavioral.chain import build_ticket_processing_chain
from patterns.behavioral.command import CommandInvoker, AssignTicketCommand, CloseTicketCommand


class TicketSystemFacade:
    def __init__(self, ticket_service: TicketService, access_service: AccessService):
        # Facade объединяет сервисы и паттерны в одну точку входа.
        self.ticket_service = ticket_service
        self.access_service = access_service

        # Creational patterns.
        self.notification_factory = NotificationFactory()
        self.builder = TicketBuilder()
        self.director = TicketDirector(self.builder)

        # Structural patterns.
        self.category_tree = build_default_category_tree()

        # Behavioral patterns.
        self.notifier = TicketNotifier()
        self.notifier.attach(EmailObserver())
        self.notifier.attach(ManagerObserver())
        self.notifier.attach(AuditObserver())

        self.priority_context = PriorityContext(KeywordPriorityStrategy())
        self.state_context = TicketStateContext()
        self.processing_chain = build_ticket_processing_chain()
        self.command_invoker = CommandInvoker()

    def show_categories(self) -> None:
        # Composite скрыт за простым методом фасада.
        self.category_tree.display()

    def create_access_ticket(self, owner: str, notification_channel: str = "email") -> Ticket:
        # Builder создаёт сложный объект тикета.
        ticket = self.director.create_access_ticket(
            ticket_id=self.ticket_service.get_next_id(),
            owner=owner
        )

        self.ticket_service.save_ticket(ticket)

        # Factory Method создаёт нужный тип уведомления.
        notification = self.notification_factory.create_notification(notification_channel)
        notification.send(owner, f"Your access ticket #{ticket.ticket_id} has been created.")

        self.notifier.notify(ticket, "Access ticket was created.")
        return ticket

    def create_hardware_ticket(self, owner: str, notification_channel: str = "sms") -> Ticket:
        ticket = self.director.create_hardware_ticket(
            ticket_id=self.ticket_service.get_next_id(),
            owner=owner
        )

        self.ticket_service.save_ticket(ticket)

        notification = self.notification_factory.create_notification(notification_channel)
        recipient = "+37360000000" if notification_channel == "sms" else owner
        notification.send(recipient, f"Your hardware ticket #{ticket.ticket_id} has been created.")

        self.notifier.notify(ticket, "Hardware ticket was created.")
        return ticket

    def calculate_priority_by_keywords(self, ticket: Ticket) -> None:
        # Strategy: приоритет рассчитывается по ключевым словам.
        self.priority_context.set_strategy(KeywordPriorityStrategy())
        self.priority_context.apply_priority(ticket)

    def calculate_priority_by_category(self, ticket: Ticket) -> None:
        # Strategy: приоритет рассчитывается по категории.
        self.priority_context.set_strategy(CategoryPriorityStrategy())
        self.priority_context.apply_priority(ticket)

    def process_ticket(self, ticket: Ticket) -> None:
        # Chain of Responsibility: тикет проходит последовательную обработку.
        self.processing_chain.handle(ticket)
        self.notifier.notify(ticket, "Ticket was processed by responsibility chain.")

    def move_ticket_next_state(self, ticket: Ticket) -> None:
        # State: меняем состояние тикета по жизненному циклу.
        self.state_context.move_next(ticket)
        self.notifier.notify(ticket, f"Ticket status changed to {ticket.status}.")

    def assign_ticket_with_command(self, ticket: Ticket, assignee: str) -> None:
        # Command: назначение тикета оформлено как отдельная команда.
        command = AssignTicketCommand(ticket, assignee, self.notifier)
        self.command_invoker.execute_command(command)

    def close_ticket_with_command(self, ticket: Ticket) -> None:
        # Command: закрытие тикета оформлено как отдельная команда.
        command = CloseTicketCommand(ticket, self.notifier)
        self.command_invoker.execute_command(command)

    def show_command_history(self) -> None:
        self.command_invoker.show_history()

    def create_ticket_view(self, ticket: Ticket):
        # Decorator: создаём представление тикета с дополнительными метками.
        ticket_view = BaseTicketView(ticket)

        if ticket.urgent:
            ticket_view = UrgentTicketViewDecorator(ticket_view)

        if ticket.sla_response_time:
            ticket_view = SlaTicketViewDecorator(ticket_view)

        if ticket.confidential:
            ticket_view = ConfidentialTicketViewDecorator(ticket_view)

        return ticket_view

    def show_ticket_for_user(self, user: User, ticket: Ticket) -> None:
        # Proxy: проверяем доступ пользователя перед показом тикета.
        ticket_view = self.create_ticket_view(ticket)

        access_proxy = TicketAccessProxy(
            user=user,
            ticket=ticket,
            ticket_view=ticket_view,
            access_service=self.access_service
        )

        access_proxy.show_ticket()

    def show_all_tickets(self) -> None:
        # Единый метод для вывода всех тикетов.
        tickets = self.ticket_service.get_all_tickets()

        if not tickets:
            print("[Facade] No tickets in the system.")
            return

        for ticket in tickets:
            print(ticket.get_info())
            print()