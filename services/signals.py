from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from .models import SpecificDate, Availability, TimeSlotAvailability, TimeSlot
from booking.models import SpaBooking


@receiver(pre_delete, sender=SpaBooking)
def pre_delete_spa_booking(sender, instance, **kwargs):

    related_services = instance.spa_booking_services.all()

    for service in related_services:
        selected_date = service.date_and_time.date()

        try:
            time_slot = TimeSlot.objects.get(spa_service=service.spa_service, time=service.date_and_time.time())
        except TimeSlot.DoesNotExist:
            continue

        try:
            specific_date = SpecificDate.objects.get(date=selected_date)
            TimeSlotAvailability.objects.filter(
                specific_date=specific_date,
                time_slot=time_slot,
                availability__spa_service=service.spa_service
            ).update(is_available=True, is_booked=False)
        except (SpecificDate.DoesNotExist, Availability.DoesNotExist):
            pass









