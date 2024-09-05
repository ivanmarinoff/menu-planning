from django.apps import AppConfig


class PlanningConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "menu_planning.planning"

    def ready(self):
        from . import signals  # noqa