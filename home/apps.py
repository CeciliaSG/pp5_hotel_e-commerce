from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' Django app.

    Sets the default auto field type and specifies the app's name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
