from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class ServiceCategory(models.Model):
    """
    Represents a category for spa services.

    Each ServiceCategory object has a name and
    a description. Categories are used to group
    spa services together.

    Attributes:
        name (str): The name of the service category.
        description (str): A detailed description of
        the service category.

    Methods:
        __str__(): Returns the string representation of
        the service category, which is its name.


    Usage:
        This model is typically used to categorise
        spa services in a structured manner.
    """
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name


STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


class SpaService(models.Model):
    """
    Represents a spa service offered by the spa.

    Each SpaService object represents a specific spa service
    with details such as its name,
    description, price, duration, category, availability status,
    and whether it requires special
    access or not.

    Attributes:
        name (str): The name of the spa service.
        description (str): A detailed description of
        the spa service.
        price (Decimal): The price of the spa service.
        currency (str): The currency code for the price
        (default is "SEK" for Swedish Krona).
        category (ForeignKey): A foreign key relationship
        to the ServiceCategory model, categorising the spa service.
        duration (DurationField): The duration of the spa service.
        is_access (bool): Indicates whether special access is required
        for the service. employee_name (str, optional): The name of
        the employee assigned to perform the service.
        featured_image (CloudinaryField, optional): An optional
        image field for the spa service.
        status (int): The status of the spa service, either Draft (0)
        or Published (1).

    Methods:
        __str__(): Returns the string representation of the spa service,
        which is its name.

    Usage:
        This model is typically used to manage and display
        detailed informationabout each spa service offered
        by the spa.

    """

    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2)
    currency = models.CharField(
        max_length=3, default="SEK")
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE)
    duration = models.DurationField()
    is_access = models.BooleanField(default=False)
    employee_name = models.CharField(
        max_length=100, blank=True, null=True)
    featured_image = CloudinaryField(
        "image", null=True, blank=True)
    status = models.SmallIntegerField(
        choices=STATUS, default=0)

    def __str__(self):
        return self.name


class SpecificDate(models.Model):
    """
    Represents a specific date associated with
    spa service availability.

    Each SpecificDate object represents a particular
    date on which a spa service may be available,
    booked, or scheduled.

    Attributes:
        date (DateField): The specific date associated
        with spa service availability.

    Methods:
        __str__(): Returns the string representation of
        the specific date, which is the date itself.

    Usage:
        This model is typically used to manage and represent
        specific dates for spa service availability or scheduling
        purposes.

    """
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class TimeSlot(models.Model):
    """
    Represents a specific time slot associated with
    spa service availability.

    Each TimeSlot object represents a particular time slot
    during which a spa service may be scheduled or booked.

    Attributes:
        time (TimeField): The specific time associated with
        the time slot.

    Methods:
        __str__(): Returns the string representation of the time slot,
        which is the time itself.

    Usage:
        This model is typically used to manage and represent specific
        time slots for spa service scheduling or booking.

    """
    time = models.TimeField()

    def __str__(self):
        return str(self.time)

    class Meta:
        ordering = ['time'] 


class Availability(models.Model):
    """
    Represents the availability of a spa service on specific dates
    and time slots.

    Each Availability object links a spa service to multiple specific
    dates and time slots during which
    the service is available for booking or scheduling.

    Attributes:
        spa_service (ForeignKey): Reference to the SpaService object
        associated with this availability.
        specific_dates (ManyToManyField): Many-to-many relationship with
        SpecificDate objects, representing the specific dates when
        the spa service is available. time_slots (ManyToManyField):
        Many-to-many relationship with TimeSlot objects, representing
        the time slots during which the spa service is available.

    Methods:
        __str__(): Returns a string representation of the availability,
        formatted as '<spa_service_name> - Availability'.

    Usage:
        This model is typically used to manage and represent the availability
        schedule of spa services, allowing users to see when specific services
        are available for booking or scheduling.
    """
    spa_service = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    specific_dates = models.ManyToManyField("SpecificDate")
    time_slots = models.ManyToManyField(TimeSlot)

    def __str__(self):
        return f"{self.spa_service.name} - Availability"
