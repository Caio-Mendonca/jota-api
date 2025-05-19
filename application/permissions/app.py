from django.apps import AppConfig


class PermissionConfig(AppConfig):
    name = "application.permissions"

    def ready(self):
        import application.permissions.signals
