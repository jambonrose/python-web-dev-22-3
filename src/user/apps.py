"""App configuration for User"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """AppConfig; loads signals for login/logout"""

    name = "user"

    def ready(self):
        """Load signals once settings are ready"""
        import user.signals  # noqa: F401
