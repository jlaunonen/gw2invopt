from django.apps import AppConfig

__all__ = [
    "Gw2InventoryApp",
]


class Gw2InventoryApp(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gw2inv_app"
