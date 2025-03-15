from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# ✅ Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, apartment_number, password=None, **extra_fields):
        """Creates and returns a regular user with an apartment number instead of a username."""
        if not apartment_number:
            raise ValueError("The Apartment Number field must be set")

        email = extra_fields.get("email")
        if not email:
            raise ValueError("The Email field must be set")

        extra_fields["email"] = self.normalize_email(email)

        user = self.model(apartment_number=apartment_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, apartment_number, password=None, **extra_fields):
        """Creates and returns a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(apartment_number, password=password, **extra_fields)


# ✅ Custom User Model
class CustomUser(AbstractUser):
    username = None  # Remove default username field
    apartment_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15, unique=True)
    contact_info = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "apartment_number"  # Authenticate with apartment_number
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "mobile_number"]

    objects = CustomUserManager()

    # Related names to avoid clashes with Django's default user model
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.apartment_number}"


# ✅ Tenant Model (Simplified)
class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tenant")

    def __str__(self):
        return f"Tenant: {self.user.first_name} {self.user.last_name} - {self.user.apartment_number}"


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


# ✅ Payment Model
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.user.apartment_number}"


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


# ✅ Notification Model
class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="notifications", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.tenant.user.apartment_number}"
