import uuid
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import make_aware

from services.models import SpaService, SpecificDate, Availability
from accounts.models import CustomerProfile


# Create your models here.

class SpaBooking(models.Model):
    """
    Represents a booking made by a customer
    for a spa service.

    Each booking contains information about
    the customer, including their profile,
    name, email, and phone number. Additionally,
    it includes details about the booking,
    such as the date and time of the appointment,
    a unique booking number generated
    using UUID, the total cost of the booking, and
    a reference to the payment transaction
    processed through Stripe.
    """
    booking_number = models.CharField(
        max_length=35, null=False, editable=False)
    customer_profile = models.ForeignKey(
        CustomerProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='spa_bookings')
    customer_name = models.CharField(
        max_length=50, null=False, blank=False)
    email = models.EmailField(
        max_length=254, null=False, blank=False)
    phone_number = models.CharField(
        max_length=20, null=False, blank=False)
    date_and_time = models.DateTimeField()
    booking_date = models.DateTimeField(
        auto_now_add=True)
    booking_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(
        null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_booking_number(self):
        """
        Generate a random, unique booking number using UUID
        """
        return uuid.uuid4().hex[:8].upper()

    def update_total(self):
        """
        Update the total cost of the spa booking.

        This method recalculates the total cost of
        the spa booking each time a change is made
        to the booking, such as adding or removing
        services.

        Note:
            This method should be called whenever
            changes are made to the booking to ensure
            accurate total calculations.

        Returns:
            None
        """
        total = self.spa_booking_services.aggregate(
            total=models.Sum('spa_service_total')
        )['total'] or Decimal('0.00')
        self.booking_total = total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to
        set the booking number
        if it hasn't been set already.
        """
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        super().save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        """
        Override the delete method to mark time slots as available and not booked again.
        """

        print("Deleting SpaBooking and updating availability...")

        related_services = self.spa_booking_services.all()
        for service in related_services:
            time_slot = service.spa_service
            selected_date = service.date_and_time.date()

            try:
                specific_date = SpecificDate.objects.get(date=selected_date)
                availability = Availability.objects.get(
                    spa_service=service.spa_service,
                    specific_dates=specific_date
                )
                TimeSlotAvailability.objects.filter(
                    availability=availability,
                    specific_date=specific_date,
                    time_slot=time_slot
                ).update(is_available=True, is_booked=False)
            except (SpecificDate.DoesNotExist, Availability.DoesNotExist):
                pass

        super().delete(*args, **kwargs)
        

    def __str__(self):
        return self.booking_number


class SpaBookingServices(models.Model):

    """
    Represents an individual service or service
    booked within a spa booking.

    Each booking service includes a reference to
    the spa service booked, the quantity,
    and the total cost for that service.

    Attributes:
        spa_service (SpaService): The spa service booked.
        quantity: The quantity of the spa service booked.
        total_cost: The total cost for the booked spa service(s).
        spa_booking (SpaBooking): The spa booking associated
        with this service.
    """

    spa_service = models.ForeignKey(
        SpaService, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    spa_service_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0'))
    spa_booking = models.ForeignKey(
        'SpaBooking', related_name='spa_booking_services',
        null=False, blank=False, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.date_and_time:
            self.date_and_time = timezone.now()
        elif timezone.is_naive(self.date_and_time):
            self.date_and_time = make_aware(self.date_and_time)

        self.spa_service_total = self.spa_service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.spa_service.name} x {self.quantity}'

