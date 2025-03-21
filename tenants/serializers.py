from rest_framework import serializers
from tenants.models import Tenant
from main.models import CustomUser

class TenantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    address = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'mobile_number',
            'contact_info', 'address', 'lease_start_date', 'lease_end_date'
        ]

    def get_address(self, obj):
        return obj.user.apartment_number  # Fetch apartment number as address

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    def get_mobile_number(self, obj):
        return obj.user.mobile_number  # Assuming `mobile_number` is a field in CustomUser
