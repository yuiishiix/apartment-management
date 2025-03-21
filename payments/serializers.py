from rest_framework import serializers
from payments.models import Payment  # Updated import
from decimal import Decimal

from tenants.models import Tenant


# ✅ Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))  # Fix applied ✅

    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'method']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'payment_date', 'method', 'receipt_number']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)


class LateFeeAssessmentSerializer(serializers.Serializer):
    apartment_number = serializers.CharField(max_length=255)  # Assuming apartment number is a string field
    overdue_days = serializers.IntegerField()
    calculated_late_fee = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        overdue_days = data.get('overdue_days')
        if overdue_days < 0:
            raise serializers.ValidationError("Overdue days cannot be negative.")
        return data

    def calculate_late_fee(self, payment, overdue_days):
        # Example logic: $5 per day overdue
        late_fee_per_day = Decimal('5.00')
        return late_fee_per_day * overdue_days

    def create(self, validated_data):
        apartment_number = validated_data['apartment_number']
        overdue_days = validated_data['overdue_days']

        try:
            # Find the tenant by apartment number
            tenant = Tenant.objects.get(apartment_number=apartment_number)

            # Retrieve the payment associated with the tenant
            payment = Payment.objects.get(tenant=tenant)

        except Tenant.DoesNotExist:
            raise serializers.ValidationError("No tenant found with the given apartment number.")
        except Payment.DoesNotExist:
            raise serializers.ValidationError("No payment found for the given tenant.")

        # Calculate the late fee
        calculated_late_fee = self.calculate_late_fee(payment, overdue_days)

        # Optionally, update the payment record with the late fee
        payment.late_fee = calculated_late_fee
        payment.save()

        # Return the response with the calculated late fee
        return {'apartment_number': apartment_number, 'overdue_days': overdue_days, 'calculated_late_fee': calculated_late_fee}
