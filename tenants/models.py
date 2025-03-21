from django.db import models
from main.models import CustomUser


# ✅ Tenant Model (Simplified)
class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tenant")

    def __str__(self):
        return f"Tenant: {self.user.first_name} {self.user.last_name} - {self.user.apartment_number}"
