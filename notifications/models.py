from django.db import models
from tenants.models import Tenant  # Assuming Tenant model exists

class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="notifications", on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, default="general")  # Set a default value here
    message_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.tenant.user.apartment_number}"


class Announcement(models.Model):
    content = models.TextField()  # The content of the announcement
    date_posted = models.DateTimeField(auto_now_add=True)  # The date the announcement was posted
    is_active = models.BooleanField(default=True)  # Whether the announcement is still active or not

    def __str__(self):
        return f"Announcement posted on {self.date_posted}"