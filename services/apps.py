from django.apps import AppConfig


class ServicesConfig(AppConfig):
    """
    Configuration class for the 'services' Django app.

    This class sets up the configuration for the 'services'
    application. It specifies the default primary key field
    type and ensures that the application's signals
    are imported and ready when the application is initialised.

    Attributes:
    - default_auto_field: Specifies the type of auto field
    to use for primary keys.
    - name: The name of the application.

    Methods:
    - ready(): This method is overridden to import the signals
    module, ensuring that the application's signals are connected
    and ready to use when the application starts.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'

    def ready(self):
        import services.signals

