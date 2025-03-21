from django.db import models
from tenants.models import Tenant


# ✅ Complaint Model
class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="complaints", on_delete=models.CASCADE)
    description = models.TextField()
    priority_level = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
    )
    status = models.CharField(
        max_length=20,
        choices=[("submitted", "Submitted"), ("resolved", "Resolved")],
        default="submitted",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint from {self.tenant.user.apartment_number} - {self.status}"
