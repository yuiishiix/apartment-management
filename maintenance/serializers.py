from rest_framework import serializers
from maintenance.models import MaintenanceRequest  # Updated import

# ✅ Maintenance Request Serializer
class MaintenanceRequestSerializer(serializers.ModelSerializer):
    urgency_level = serializers.ChoiceField(choices=['low', 'medium', 'high'], default='medium')

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'tenant', 'description', 'urgency_level', 'status', 'created_at']

    def create(self, validated_data):
        return MaintenanceRequest.objects.create(**validated_data)
