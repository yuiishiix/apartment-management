from django.db import models
from tenants.models import Tenant


# ✅ Maintenance Request Model
class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="maintenance_requests", on_delete=models.CASCADE)
    description = models.TextField()
    urgency_level = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.tenant.user.apartment_number} - {self.status}"
