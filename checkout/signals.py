from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from booking.models import SpaBookingServices, SpaBooking


@receiver(post_save, sender=SpaBookingServices)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update booking total on SpaService update/create
    """
    print(f"Signal received for {instance.spa_booking} on save")
    instance.spa_booking.update_total()


@receiver(post_delete, sender=SpaBookingServices)
def update_on_delete(sender, instance, **kwargs):
    """
    Update booking total on spaservices delete
    """
    instance.spa_booking.update_total()
