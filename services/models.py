from django.db import models
from django.contrib.auth.models import User
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
    name = models.CharField(max_length=300, unique=True)
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

    STATUS_CHOICES = (
        (0, 'Unavailable'),
        (1, 'Available'),
    )

    name = models.CharField(max_length=300, unique=True)
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
        choices=STATUS_CHOICES, default=1)


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

    class Meta:
        ordering = ['date']


class TimeSlot(models.Model):
    time = models.TimeField()
    spa_service = models.ForeignKey(SpaService, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.spa_service.name} - {self.time}"

    class Meta:
        unique_together = ('time', 'spa_service')
        ordering = ['time']

    def mark_available_for_date(self, specific_date):
        availability, created = Availability.objects.get_or_create(spa_service=self.spa_service)
        TimeSlotAvailability.objects.update_or_create(
            availability=availability,
            specific_date=specific_date,
            time_slot=self,
            defaults={'is_available': True}
        )

    def mark_unavailable_for_date(self, specific_date):
        availability, created = Availability.objects.get_or_create(spa_service=self.spa_service)
        TimeSlotAvailability.objects.update_or_create(
            availability=availability,
            specific_date=specific_date,
            time_slot=self,
            defaults={'is_available': False}
        )


class TimeSlotAvailability(models.Model):
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE)
    specific_date = models.ForeignKey(SpecificDate, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('availability', 'specific_date', 'time_slot')


class Availability(models.Model):
    spa_service = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    specific_dates = models.ManyToManyField(SpecificDate)
    time_slots = models.ManyToManyField(TimeSlot, through=TimeSlotAvailability)

    def save_model(self, request, obj, form, change):
        if Availability.objects.filter(spa_service=obj.spa_service).exists() and not change:
            raise ValidationError(f"The spa service '{obj.spa_service}' is already available.")
        super().save_model(request, obj, form, change)

    def __str__(self):
        return f"{self.spa_service.name} - Availability"


class Review(models.Model):
    """
    From "I Think therfore I blog".
    Lets logged-in users review spa services.
    """
    spa_service = models.ForeignKey(
        SpaService, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Review {self.body} by {self.author}"