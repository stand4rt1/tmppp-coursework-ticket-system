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


class TicketSystemFacade:
    def __init__(self, ticket_service: TicketService, access_service: AccessService):
        # Facade объединяет основные сервисы и скрывает внутреннюю сложность.
        self.ticket_service = ticket_service
        self.access_service = access_service
        self.notification_factory = NotificationFactory()
        self.builder = TicketBuilder()
        self.director = TicketDirector(self.builder)
        self.category_tree = build_default_category_tree()

    def show_categories(self) -> None:
        # Клиенту не нужно знать, как устроено дерево категорий.
        self.category_tree.display()

    def create_access_ticket(self, owner: str, notification_channel: str = "email") -> Ticket:
        # Создаём тикет через Builder/Director.
        ticket = self.director.create_access_ticket(
            ticket_id=self.ticket_service.get_next_id(),
            owner=owner
        )

        self.ticket_service.save_ticket(ticket)

        # Уведомление создаётся через Factory Method.
        notification = self.notification_factory.create_notification(notification_channel)
        notification.send(owner, f"Your access ticket #{ticket.ticket_id} has been created.")

        return ticket

    def create_hardware_ticket(self, owner: str, notification_channel: str = "sms") -> Ticket:
        ticket = self.director.create_hardware_ticket(
            ticket_id=self.ticket_service.get_next_id(),
            owner=owner
        )

        self.ticket_service.save_ticket(ticket)

        notification = self.notification_factory.create_notification(notification_channel)

        # В учебном проекте для SMS используем условный номер.
        recipient = "+37360000000" if notification_channel == "sms" else owner
        notification.send(recipient, f"Your hardware ticket #{ticket.ticket_id} has been created.")

        return ticket

    def create_ticket_view(self, ticket: Ticket):
        # Базовое отображение тикета.
        ticket_view = BaseTicketView(ticket)

        # Decorator добавляет визуальные метки без изменения класса Ticket.
        if ticket.urgent:
            ticket_view = UrgentTicketViewDecorator(ticket_view)

        if ticket.sla_response_time:
            ticket_view = SlaTicketViewDecorator(ticket_view)

        if ticket.confidential:
            ticket_view = ConfidentialTicketViewDecorator(ticket_view)

        return ticket_view

    def show_ticket_for_user(self, user: User, ticket: Ticket) -> None:
        # Proxy проверяет доступ перед показом тикета.
        ticket_view = self.create_ticket_view(ticket)

        access_proxy = TicketAccessProxy(
            user=user,
            ticket=ticket,
            ticket_view=ticket_view,
            access_service=self.access_service
        )

        access_proxy.show_ticket()

    def show_all_tickets(self) -> None:
        tickets = self.ticket_service.get_all_tickets()

        if not tickets:
            print("[Facade] No tickets in the system.")
            return

        for ticket in tickets:
            print(ticket.get_info())
            print()