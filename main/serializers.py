from rest_framework import serializers
from .models import CustomUser



# ✅ User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'apartment_number', 'email', 'password', 'first_name', 'last_name', 'mobile_number']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove password from validated_data
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

