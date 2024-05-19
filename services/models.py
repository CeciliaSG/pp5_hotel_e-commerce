from django.db import models

# Create your models here.

class ServiceCategory(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name


class SpaService(models.Model):
   name = models.CharField(max_length=300)
   description = models.TextField()
   price = models.DecimalField(max_digits=6, decimal_places=2)
   category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
   date_and_time = models.DateTimeField()
   duration = models.DurationField()
   is_access = models.BooleanField(default=False)
   available = models.BooleanField(default=True)

   def __str__(self):
        return self.name



