from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomerProfile(models.Model):
    """
    From Boutique Ado Walkthrough.

    Represents a customer profile that extends the default
    Django User model.

    This model is used to store  information related to the user.

    Attributes:
        user (OneToOneField): A one-to-one relationship
        with the Django User model.
        default_phone_number (CharField):
        The default phone number of the user.
        email (EmailField): The email address of the user.

    Methods:
        __str__(): Returns the username of the associated
        User model.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
            max_length=20, null=True, blank=True)
    email = models.EmailField(
            max_length=254, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True,
                            blank=True)

    def __str__(self):
        return self.user.username

    def get_email(self):
        return self.email if self.email else self.user.email

