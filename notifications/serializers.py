from rest_framework import serializers
from notifications.models import Notification  # Updated import

# ✅ Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'tenant', 'message', 'created_at', 'is_read']

    def update(self, instance, validated_data):
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
