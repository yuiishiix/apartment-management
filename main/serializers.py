from .models import Tenant, MaintenanceRequest, Payment, Complaint, Notification
from django.contrib.auth.models import User
from rest_framework import serializers

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Creating the user with a hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Tenant Serializer
class TenantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'user', 'name', 'contact_info', 'email', 'address']

    # You can add custom validation for Tenant, if needed.
    def create(self, validated_data):
        tenant = Tenant.objects.create(**validated_data)
        return tenant


# Maintenance Request Serializer
class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'tenant', 'description', 'urgency_level', 'status', 'created_at']

    def validate_urgency_level(self, value):
        # Optional: add validation for urgency_level
        if value not in ['Low', 'Medium', 'High']:
            raise serializers.ValidationError("Invalid urgency level")
        return value


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'method']

    def validate_amount(self, value):
        # Optional: Add validation for the amount to ensure it’s greater than zero
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value


# Complaint Serializer
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'tenant', 'description', 'priority_level', 'status', 'created_at']

    def validate_priority_level(self, value):
        # Optional: Add validation for priority_level
        if value not in ['Low', 'Medium', 'High']:
            raise serializers.ValidationError("Invalid priority level")
        return value


# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'tenant', 'message', 'created_at', 'is_read']

    def update(self, instance, validated_data):
        # Optional: custom logic to update a notification
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
