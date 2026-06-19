from dataclasses import dataclass


@dataclass
class Ticket:
    ticket_id: int
    title: str
    description: str
    category: str
    owner: str
    ticket_type: str
    priority: str = "Undefined"
    assignee: str = "Unassigned"
    status: str = "New"
    confidential: bool = False
    sla_response_time: str | None = None
    urgent: bool = False

    def get_info(self) -> str:
        # Преобразуем булевые значения в более понятный текст для вывода.
        confidential_text = "Yes" if self.confidential else "No"
        urgent_text = "Yes" if self.urgent else "No"
        sla_text = self.sla_response_time if self.sla_response_time else "Not set"

        # Формируем полное описание тикета.
        return (
            f"Ticket #{self.ticket_id}\n"
            f"Type: {self.ticket_type}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Category: {self.category}\n"
            f"Owner: {self.owner}\n"
            f"Priority: {self.priority}\n"
            f"Assignee: {self.assignee}\n"
            f"Status: {self.status}\n"
            f"Urgent: {urgent_text}\n"
            f"SLA Response Time: {sla_text}\n"
            f"Confidential: {confidential_text}"
        )