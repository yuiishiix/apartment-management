from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='maintenance_requests', on_delete=models.CASCADE)
    description = models.TextField()
    urgency_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.tenant.name} - {self.status}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.name}"

class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='complaints', on_delete=models.CASCADE)
    description = models.TextField()
    priority_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('resolved', 'Resolved')], default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint from {self.tenant.name} - {self.status}"

class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.tenant.name}"
