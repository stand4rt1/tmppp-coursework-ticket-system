from core.ticket import Ticket


class PriorityStrategy:
    def calculate_priority(self, ticket: Ticket) -> str:
        raise NotImplementedError("Subclasses must implement this method.")


class CategoryPriorityStrategy(PriorityStrategy):
    def calculate_priority(self, ticket: Ticket) -> str:
        # Приоритет определяется по категории тикета.
        category = ticket.category.lower()

        if "access" in category or "security" in category:
            return "High"

        if "hardware" in category:
            return "Medium"

        return "Low"


class KeywordPriorityStrategy(PriorityStrategy):
    def calculate_priority(self, ticket: Ticket) -> str:
        # Приоритет определяется по ключевым словам в названии и описании.
        text = f"{ticket.title} {ticket.description}".lower()

        if "cannot login" in text or "blocked" in text or "urgent" in text:
            return "High"

        if "printer" in text or "slow" in text:
            return "Medium"

        return "Low"


class PriorityContext:
    def __init__(self, strategy: PriorityStrategy):
        # Контекст хранит выбранную стратегию расчёта приоритета.
        self.strategy = strategy

    def set_strategy(self, strategy: PriorityStrategy) -> None:
        # Стратегию можно заменить во время работы программы.
        self.strategy = strategy

    def apply_priority(self, ticket: Ticket) -> None:
        # Применяем выбранный алгоритм к тикету.
        ticket.priority = self.strategy.calculate_priority(ticket)
        print(f"[Strategy] Priority for ticket #{ticket.ticket_id}: {ticket.priority}")