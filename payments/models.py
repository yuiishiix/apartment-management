from django.db import models
from tenants.models import Tenant


# ✅ Payment Model
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.user.apartment_number}"
