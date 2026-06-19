class AppConfig:
    # Храним единственный экземпляр конфигурации.
    # Это реализация паттерна Singleton.
    _instance = None

    def __new__(cls):
        # Если объект конфигурации ещё не создан, создаём его один раз.
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)

            # Общие настройки приложения.
            cls._instance.app_name = "Coursework Ticket System"
            cls._instance.default_notification_channel = "email"
            cls._instance.max_open_tickets_per_user = 5
            cls._instance.support_department = "Technical Support"

        # При повторном создании возвращается тот же самый объект.
        return cls._instance

    def get_info(self) -> str:
        # Возвращаем настройки системы в удобном виде.
        return (
            f"Application: {self.app_name}\n"
            f"Default notification channel: {self.default_notification_channel}\n"
            f"Max open tickets per user: {self.max_open_tickets_per_user}\n"
            f"Support department: {self.support_department}"
        )