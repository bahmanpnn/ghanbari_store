from django.apps import AppConfig


class ProductModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_module'

    def ready(self):
        import product_module.signals  # Ensures the signals are loaded
