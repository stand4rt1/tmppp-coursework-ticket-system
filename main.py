from config.app_config import AppConfig
from core.user import User
from services.ticket_service import TicketService
from services.access_service import AccessService

from patterns.creational.builder import TicketBuilder, TicketDirector
from patterns.creational.factory_method import NotificationFactory


def main():
    print("=== Coursework Ticket System: Creational Patterns Check ===\n")

    # Singleton: единая конфигурация приложения.
    config1 = AppConfig()
    config2 = AppConfig()

    print("=== Singleton: Application Configuration ===")
    print(config1.get_info())
    print(f"Singleton check: config1 is config2 -> {config1 is config2}")

    ticket_service = TicketService()

    # Builder: пошаговая сборка сложных тикетов.
    print("\n=== Builder: Ticket Creation ===")
    builder = TicketBuilder()
    director = TicketDirector(builder)

    access_ticket = director.create_access_ticket(
        ticket_id=ticket_service.get_next_id(),
        owner="ilia"
    )

    hardware_ticket = director.create_hardware_ticket(
        ticket_id=ticket_service.get_next_id(),
        owner="admin"
    )

    ticket_service.save_ticket(access_ticket)
    ticket_service.save_ticket(hardware_ticket)

    print()
    print(access_ticket.get_info())
    print()
    print(hardware_ticket.get_info())

    # Factory Method: создание разных каналов уведомлений.
    print("\n=== Factory Method: Notification Creation ===")
    notification_factory = NotificationFactory()

    email_notification = notification_factory.create_notification("email")
    sms_notification = notification_factory.create_notification("sms")
    messenger_notification = notification_factory.create_notification("messenger")

    email_notification.send("ilia", "Your access ticket has been created.")
    sms_notification.send("+37360000000", "Your hardware ticket has been created.")
    messenger_notification.send("admin", "A new ticket has been assigned to your department.")

    # Базовая проверка доступа.
    print("\n=== Access Service Check ===")
    owner = User(username="ilia", role="user")
    admin = User(username="admin", role="admin")
    stranger = User(username="alex", role="user")

    access_service = AccessService()

    print(f"Owner can view access ticket: {access_service.can_view_ticket(owner, access_ticket)}")
    print(f"Admin can view access ticket: {access_service.can_view_ticket(admin, access_ticket)}")
    print(f"Stranger can view access ticket: {access_service.can_view_ticket(stranger, access_ticket)}")


if __name__ == "__main__":
    main()