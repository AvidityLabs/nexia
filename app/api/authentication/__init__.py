from django.apps import AppConfig




class APIAppConfig(AppConfig):
    name = 'api.authentication'
    label = 'api'
    verbose_name = 'API'

    def ready(self):
        import api.signals

# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'api.authentication.APIAppConfig'