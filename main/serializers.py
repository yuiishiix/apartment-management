from rest_framework import serializers
from .models import Tenant, MaintenanceRequest, Payment, Complaint, Notification

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'contact_info', 'email', 'address']

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'tenant', 'description', 'urgency_level', 'status', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'method']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['id', 'tenant', 'description', 'priority_level', 'status', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'tenant', 'message', 'created_at', 'is_read']
