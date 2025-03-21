import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Payment, Tenant
from .serializers import PaymentSerializer, PaymentReceiptSerializer, LateFeeAssessmentSerializer


class TenantPaymentsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenantId):
        try:
            tenant = Tenant.objects.get(id=tenantId)
            payments = Payment.objects.filter(tenant=tenant)
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class SubmitPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tenantId):
        data = request.data
        try:
            tenant = Tenant.objects.get(id=tenantId)
            payment = Payment.objects.create(
                tenant=tenant,
                amount=data['amount'],
                method=data['method']
            )
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)


class PaymentReceiptView(APIView):

    def get(self, request, paymentId):
        try:
            # Retrieve the payment using paymentId
            payment = Payment.objects.get(id=paymentId)

            # Serialize the payment data (could be expanded to generate a receipt)
            serializer = PaymentReceiptSerializer(payment)

            # Return the payment receipt data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


logger = logging.getLogger(__name__)


class AssessLateFeeView(APIView):
    def post(self, request, apartment_number):
        print("Received data:", request.data)
        try:
            overdue_days = request.data.get("overdue_days")
            print(f"Overdue days: {overdue_days}")

            # Your logic here for assessing late fees
            if not overdue_days:
                return Response({"error": "Overdue days is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Perform the logic (e.g., calculate late fee)
            # For example, assume you calculate the late fee and return it:
            late_fee = overdue_days * 10  # Example calculation
            print(f"Late fee: {late_fee}")

            return Response({"late_fee": late_fee}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", e)
            return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeletePaymentMethodView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, payment_id):
        try:
            # Retrieve the payment method based on the payment_id
            payment = Payment.objects.get(id=payment_id)

            # Delete the payment method
            payment.delete()

            # Return success message
            return Response({"message": "Payment method deleted successfully."}, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response({"error": "Payment method not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)