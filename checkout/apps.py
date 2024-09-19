from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Configuration class for the 'checkout' Django app.

    Sets the default auto field type and imports signals when the app is ready.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        import checkout.signals

