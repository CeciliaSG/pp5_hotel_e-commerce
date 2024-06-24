from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomerProfile(models.Model):
    """
    From Boutique Ado Walkthrough.

    Represents a customer profile that extends the default Django User model.

    This model is used to store  information related to the user.

    Attributes:
        user (OneToOneField): A one-to-one relationship
        with the Django User model.
        default_phone_number (CharField):
        The default phone number of the user.
        email (EmailField): The email address of the user.

    Methods:
        __str__(): Returns the username of the associated User model.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
            max_length=20, null=True, blank=True)
    email = models.EmailField(
            max_length=254, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance, email=instance.email)
    instance.customerprofile.save()
