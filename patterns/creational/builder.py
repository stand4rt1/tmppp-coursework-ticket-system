from core.ticket import Ticket


class TicketBuilder:
    def __init__(self):
        # При создании Builder сбрасываем все временные данные.
        self.reset()

    def reset(self):
        # Значения по умолчанию для будущего тикета.
        # После build() объект снова будет сброшен.
        self._ticket_id = None
        self._title = ""
        self._description = ""
        self._category = ""
        self._owner = ""
        self._ticket_type = "General"
        self._priority = "Undefined"
        self._assignee = "Unassigned"
        self._status = "New"
        self._confidential = False
        self._sla_response_time = None
        self._urgent = False
        return self

    def set_id(self, ticket_id: int):
        self._ticket_id = ticket_id
        return self

    def set_title(self, title: str):
        self._title = title
        return self

    def set_description(self, description: str):
        self._description = description
        return self

    def set_category(self, category: str):
        self._category = category
        return self

    def set_owner(self, owner: str):
        self._owner = owner
        return self

    def set_ticket_type(self, ticket_type: str):
        self._ticket_type = ticket_type
        return self

    def set_priority(self, priority: str):
        self._priority = priority
        return self

    def set_assignee(self, assignee: str):
        self._assignee = assignee
        return self

    def set_status(self, status: str):
        self._status = status
        return self

    def mark_confidential(self):
        # Отмечаем тикет как конфиденциальный.
        self._confidential = True
        return self

    def set_sla_response_time(self, response_time: str):
        # Указываем время реакции по SLA.
        self._sla_response_time = response_time
        return self

    def mark_urgent(self):
        # Отмечаем тикет как срочный.
        self._urgent = True
        return self

    def build(self) -> Ticket:
        # Минимальная проверка, чтобы не создать пустой тикет.
        if self._ticket_id is None:
            raise ValueError("Ticket ID is required.")

        if not self._title:
            raise ValueError("Ticket title is required.")

        if not self._owner:
            raise ValueError("Ticket owner is required.")

        ticket = Ticket(
            ticket_id=self._ticket_id,
            title=self._title,
            description=self._description,
            category=self._category,
            owner=self._owner,
            ticket_type=self._ticket_type,
            priority=self._priority,
            assignee=self._assignee,
            status=self._status,
            confidential=self._confidential,
            sla_response_time=self._sla_response_time,
            urgent=self._urgent
        )

        # После создания тикета Builder готов к сборке нового объекта.
        self.reset()
        return ticket


class TicketDirector:
    def __init__(self, builder: TicketBuilder):
        self.builder = builder

    def create_access_ticket(self, ticket_id: int, owner: str) -> Ticket:
        # Готовый сценарий сборки тикета для проблемы доступа.
        return (
            self.builder
            .set_id(ticket_id)
            .set_title("Cannot login to account")
            .set_description("User cannot access the internal support portal.")
            .set_category("Support Department / IT / Access / Login Problems")
            .set_owner(owner)
            .set_ticket_type("Access")
            .mark_urgent()
            .set_sla_response_time("2 hours")
            .build()
        )

    def create_hardware_ticket(self, ticket_id: int, owner: str) -> Ticket:
        # Готовый сценарий сборки тикета для аппаратной проблемы.
        return (
            self.builder
            .set_id(ticket_id)
            .set_title("Printer works slowly")
            .set_description("The office printer is slow during document printing.")
            .set_category("Support Department / IT / Hardware / Printer Problems")
            .set_owner(owner)
            .set_ticket_type("Hardware")
            .set_sla_response_time("6 hours")
            .build()
        )