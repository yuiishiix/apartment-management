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



