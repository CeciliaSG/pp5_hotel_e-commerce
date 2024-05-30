from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
import uuid
from services.models import SpaService
from django.db.models import Sum

# Create your models here.

class SpaBooking(models.Model):
    """
    Represents a booking made by a customer for a spa service.

    Each booking contains information about the customer, including their profile,
    name, email, and phone number. Additionally, it includes details about the booking,
    such as the date and time of the appointment, a unique booking number generated
    using UUID, the total cost of the booking, and a reference to the payment transaction
    processed through Stripe.
    """
    booking_number = models.CharField(max_length=35, null=False, editable=False)
    customer_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    date_and_time = models.DateTimeField()
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    def _generate_booking_number(self):
        """
        Generate a random, unique booking number using UUID
        """
        return uuid.uuid4().hex.upper()


    def update_total(self):
        """
        Update the total cost of the spa booking.

        This method recalculates the total cost of the spa booking each time a change is made
        to the booking, such as adding or removing services.

        Note:
            This method should be called whenever changes are made to the booking to ensure
            accurate total calculations.

        Returns:
            None
        """
        self.booking_total = self.spa_booking_services.aggregate(models.Sum('spa_service_total'))['spa_service_total__sum'] or Decimal('0.00')

        self.save()    


    def save(self, *args, **kwargs):
        """
        Override the original save method to set the booking number
        if it hasn't been set already.
        """
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number    


class SpaBookingServices(models.Model):

    """
    Represents an individual service or service booked within a spa booking.

    Each booking service includes a reference to the spa service booked, the quantity,
    and the total cost for that particular service.

    Attributes:
        spa_service (SpaService): The spa service booked.
        quantity: The quantity of the spa service booked.
        total_cost: The total cost for the booked spa service(s).
        spa_booking (SpaBooking): The spa booking associated with this service.
    """

    spa_service = models.ForeignKey(SpaService, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    spa_service_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    spa_booking = models.ForeignKey('SpaBooking', related_name='spa_booking_services', null=False, blank=False, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):

        self.spa_service_total = self.spa_service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
            return f'{self.spa_service.name} x {self.quantity}'
