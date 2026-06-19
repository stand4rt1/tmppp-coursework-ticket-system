from dataclasses import dataclass


@dataclass
class Category:
    name: str

    def get_name(self) -> str:
        # Возвращаем название категории.
        return self.name