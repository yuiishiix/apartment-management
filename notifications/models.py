from django.db import models
from tenants.models import Tenant


# ✅ Notification Model
class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="notifications", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.tenant.user.apartment_number}"
