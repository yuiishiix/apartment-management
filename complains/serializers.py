from rest_framework import serializers
from complains.models import Complaint  # Updated import

# ✅ Complaint Serializer
class ComplaintSerializer(serializers.ModelSerializer):
    priority_level = serializers.ChoiceField(choices=['low', 'medium', 'high'], default='medium')

    class Meta:
        model = Complaint
        fields = ['id', 'tenant', 'description', 'priority_level', 'status', 'created_at']

    def create(self, validated_data):
        return Complaint.objects.create(**validated_data)
