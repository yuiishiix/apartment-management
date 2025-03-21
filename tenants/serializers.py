from rest_framework import serializers
from tenants.models import Tenant  # Updated import
from main.models import CustomUser

# ✅ Tenant Serializer
class TenantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Tenant
        fields = ['id', 'user', 'contact_info', 'address', 'lease_start_date', 'lease_end_date']

    def create(self, validated_data):
        return Tenant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.contact_info = validated_data.get('contact_info', instance.contact_info)
        instance.address = validated_data.get('address', instance.address)
        instance.lease_start_date = validated_data.get('lease_start_date', instance.lease_start_date)
        instance.lease_end_date = validated_data.get('lease_end_date', instance.lease_end_date)
        instance.save()
        return instance
