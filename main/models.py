from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model to replace the default User model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    apartment_number = models.CharField(max_length=50, unique=True)
    username = None  # Remove the default 'username' field
    email = models.EmailField(unique=True)  # Retain email as a secondary field for contact purposes

    USERNAME_FIELD = 'apartment_number'  # Set apartment_number as the unique field for authentication
    REQUIRED_FIELDS = ['email', 'password']  # Email and password will be required fields during user creation

    # Add related_name to avoid clash with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoid clash with the default User model's 'groups'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoid clash with the default User model's 'user_permissions'
        blank=True
    )

    def __str__(self):
        return self.apartment_number


# Tenant model modified to link to the CustomUser model instead of using the email directly
class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # One-to-one relationship with CustomUser
    contact_info = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.apartment_number  # Using the apartment number from CustomUser as the identifier


class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='maintenance_requests', on_delete=models.CASCADE)
    description = models.TextField()
    urgency_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'),
                                                      ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.tenant.user.apartment_number} - {self.status}"


class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.user.apartment_number}"


class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='complaints', on_delete=models.CASCADE)
    description = models.TextField()
    priority_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('resolved', 'Resolved')],
                              default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint from {self.tenant.user.apartment_number} - {self.status}"


class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.tenant.user.apartment_number}"
