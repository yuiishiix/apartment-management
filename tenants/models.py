from django.db import models
from main.models import CustomUser

class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tenant")

    contact_info = models.CharField(max_length=255, blank=True, null=True)
    lease_start_date = models.DateField(blank=True, null=True)
    lease_end_date = models.DateField(blank=True, null=True)

    @property
    def address(self):
        return self.user.apartment_number  # Automatically returns the apartment number

    def __str__(self):
        return f"Tenant: {self.user.first_name} {self.user.last_name} - {self.user.apartment_number}"
