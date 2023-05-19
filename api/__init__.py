from django.apps import AppConfig


class APIAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.signals  # Replace with your actual signals module path
