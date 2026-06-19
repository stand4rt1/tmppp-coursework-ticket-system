from config.app_config import AppConfig
from core.user import User
from core.ticket import Ticket
from services.ticket_service import TicketService
from services.access_service import AccessService


def main():
    print("=== Coursework Ticket System: Base Check ===\n")

    # Проверяем работу Singleton.
    # Оба объекта должны ссылаться на один и тот же экземпляр конфигурации.
    config1 = AppConfig()
    config2 = AppConfig()

    print(config1.get_info())
    print(f"\nSingleton check: config1 is config2 -> {config1 is config2}")

    # Создаём сервис для хранения тикетов.
    ticket_service = TicketService()

    # Пока создаём тикет напрямую.
    # Позже заменим это на Builder и Factory Method.
    ticket = Ticket(
        ticket_id=ticket_service.get_next_id(),
        title="Cannot login to account",
        description="User cannot access the internal support portal.",
        category="Support Department / IT / Access / Login Problems",
        owner="ilia",
        ticket_type="Access"
    )

    ticket_service.save_ticket(ticket)

    # Создаём пользователей для проверки прав доступа.
    user = User(username="ilia", role="user")
    admin = User(username="admin", role="admin")
    stranger = User(username="alex", role="user")

    access_service = AccessService()

    print()
    print(ticket.get_info())

    print("\n=== Access Check ===")
    print(f"Owner can view: {access_service.can_view_ticket(user, ticket)}")
    print(f"Admin can view: {access_service.can_view_ticket(admin, ticket)}")
    print(f"Stranger can view: {access_service.can_view_ticket(stranger, ticket)}")


if __name__ == "__main__":
    main()