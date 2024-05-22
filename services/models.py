from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class ServiceCategory(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name
        

STATUS = ((0, "Draft"), (1, "Published"),)        


class SpaService(models.Model):
   name = models.CharField(max_length=300)
   description = models.TextField()
   price = models.DecimalField(max_digits=6, decimal_places=2)
   currency = models.CharField(max_length=3, default='SEK')
   category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
   duration = models.DurationField()
   is_access = models.BooleanField(default=False)
   available = models.BooleanField(default=True)
   employee_name = models.CharField(max_length=100, blank=True, null=True)
   featured_image = CloudinaryField('image', null=True, blank=True)
   status = models.SmallIntegerField(choices=STATUS, default=0)


   def __str__(self):
        return self.name



