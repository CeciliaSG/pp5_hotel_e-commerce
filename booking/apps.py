from django.apps import AppConfig


class BookingConfig(AppConfig):
    """
    Configuration class for the 'booking' Django app.

    Sets the default auto field type and specifies the app's name.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
