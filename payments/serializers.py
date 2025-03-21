from rest_framework import serializers
from payments.models import Payment  # Updated import
from decimal import Decimal

# ✅ Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))  # Fix applied ✅

    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'method']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)
