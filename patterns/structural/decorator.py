class TicketViewComponent:
    def get_info(self) -> str:
        raise NotImplementedError("Subclasses must implement this method.")


class BaseTicketView(TicketViewComponent):
    def __init__(self, ticket):
        # Базовая обёртка над обычным тикетом.
        self.ticket = ticket

    def get_info(self) -> str:
        return self.ticket.get_info()


class TicketViewDecorator(TicketViewComponent):
    def __init__(self, wrapped_view: TicketViewComponent):
        # Декоратор хранит объект с тем же интерфейсом.
        self.wrapped_view = wrapped_view

    def get_info(self) -> str:
        return self.wrapped_view.get_info()


class UrgentTicketViewDecorator(TicketViewDecorator):
    def get_info(self) -> str:
        return self.wrapped_view.get_info() + "\nDisplay Label: URGENT TICKET"


class SlaTicketViewDecorator(TicketViewDecorator):
    def get_info(self) -> str:
        return self.wrapped_view.get_info() + "\nDisplay Label: SLA CONTROL ENABLED"


class ConfidentialTicketViewDecorator(TicketViewDecorator):
    def get_info(self) -> str:
        return self.wrapped_view.get_info() + "\nDisplay Label: CONFIDENTIAL DATA"