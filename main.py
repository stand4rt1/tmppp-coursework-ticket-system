from config.app_config import AppConfig
from core.user import User

from services.ticket_service import TicketService
from services.access_service import AccessService
from services.notification_service import ExternalMessengerAPI

from patterns.structural.facade import TicketSystemFacade
from patterns.structural.adapter import MessengerNotificationAdapter


def main():
    print("=== Coursework Ticket System: Full Pattern Integration Check ===\n")

    # Singleton: единая конфигурация приложения.
    config = AppConfig()
    print("=== Singleton: Application Configuration ===")
    print(config.get_info())

    ticket_service = TicketService()
    access_service = AccessService()

    # Facade: единая точка входа в систему.
    ticket_system = TicketSystemFacade(
        ticket_service=ticket_service,
        access_service=access_service
    )

    print("\n=== Composite: Ticket Categories ===")
    ticket_system.show_categories()

    print("\n=== Builder + Factory Method + Observer: Creating Tickets ===")
    access_ticket = ticket_system.create_access_ticket(
        owner="ilia",
        notification_channel="email"
    )

    hardware_ticket = ticket_system.create_hardware_ticket(
        owner="admin",
        notification_channel="sms"
    )

    print("\n=== Adapter: External Messenger API ===")
    external_api = ExternalMessengerAPI()
    messenger_adapter = MessengerNotificationAdapter(external_api)
    messenger_adapter.send(
        recipient="admin",
        message="External messenger notification was sent through adapter."
    )

    print("\n=== Strategy: Priority Calculation ===")
    ticket_system.calculate_priority_by_keywords(access_ticket)
    ticket_system.calculate_priority_by_category(hardware_ticket)

    print("\n=== Chain of Responsibility: Ticket Processing ===")
    ticket_system.process_ticket(access_ticket)
    ticket_system.process_ticket(hardware_ticket)

    print("\n=== State: Ticket Lifecycle ===")
    ticket_system.move_ticket_next_state(access_ticket)
    ticket_system.move_ticket_next_state(access_ticket)
    ticket_system.move_ticket_next_state(access_ticket)

    print("\n=== Command: Ticket Actions ===")
    ticket_system.assign_ticket_with_command(
        ticket=hardware_ticket,
        assignee="Support Team Lead"
    )

    ticket_system.close_ticket_with_command(hardware_ticket)
    ticket_system.show_command_history()

    print("\n=== Decorator + Proxy: Ticket View and Access Control ===")
    owner = User(username="ilia", role="user")
    stranger = User(username="alex", role="user")
    admin = User(username="admin", role="admin")

    print("\nOwner tries to view own ticket:")
    ticket_system.show_ticket_for_user(owner, access_ticket)

    print("\nStranger tries to view another user's ticket:")
    ticket_system.show_ticket_for_user(stranger, access_ticket)

    print("\nAdmin tries to view any ticket:")
    ticket_system.show_ticket_for_user(admin, access_ticket)

    print("\n=== Facade: All Tickets ===")
    ticket_system.show_all_tickets()


if __name__ == "__main__":
    main()