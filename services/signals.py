from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import SpecificDate, Availability, TimeSlotAvailability, TimeSlot
from booking.models import SpaBooking, SpaBookingServices


@receiver(pre_delete, sender=SpaBookingServices)
def pre_delete_spa_booking_service(sender, instance, **kwargs):
    """
    Signal to update the associated time slots' availability when a service is deleted or canceled.
    """
    selected_date = instance.date_and_time.date()

    try:
        time_slot = TimeSlot.objects.get(spa_service=instance.spa_service, time=instance.date_and_time.time())
    except TimeSlot.DoesNotExist:
        return

    try:
        specific_date = SpecificDate.objects.get(date=selected_date)
        TimeSlotAvailability.objects.filter(
            specific_date=specific_date,
            time_slot=time_slot,
            availability__spa_service=instance.spa_service
        ).update(is_available=True, is_booked=False)
    except (SpecificDate.DoesNotExist, Availability.DoesNotExist):
        pass









