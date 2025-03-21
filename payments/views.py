from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Payment, Tenant
from .serializers import PaymentSerializer

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
