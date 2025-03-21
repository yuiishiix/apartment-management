from django.db import models
from tenants.models import Tenant  # Assuming Tenant model exists


class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    facility = models.ForeignKey(Facility, related_name='bookings', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, related_name='bookings', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Booking for {self.facility.name} by {self.tenant.user.username}"

    class Meta:
        unique_together = ('facility', 'date', 'start_time')  # Prevent double booking at the same time
