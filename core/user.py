from dataclasses import dataclass


@dataclass
class User:
    username: str
    role: str

    def is_admin(self) -> bool:
        # Проверяем, является ли пользователь администратором.
        # Это понадобится для проверки доступа к тикетам.
        return self.role.lower() == "admin"

    def get_info(self) -> str:
        # Возвращаем краткую информацию о пользователе.
        return f"User: {self.username}, Role: {self.role}"