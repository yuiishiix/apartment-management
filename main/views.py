from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tenant, MaintenanceRequest, Payment, Complaint, Notification
from .serializers import TenantSerializer, MaintenanceRequestSerializer, PaymentSerializer, ComplaintSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class TenantProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenantId):
        try:
            tenant = Tenant.objects.get(id=tenantId)
            serializer = TenantSerializer(tenant)
            return Response(serializer.data)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, tenantId):
        try:
            tenant = Tenant.objects.get(id=tenantId)
            serializer = TenantSerializer(tenant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

class SubmitMaintenanceRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tenantId):
        data = request.data
        try:
            tenant = Tenant.objects.get(id=tenantId)
            maintenance_request = MaintenanceRequest.objects.create(
                tenant=tenant,
                description=data['description'],
                urgency_level=data['urgency_level']
            )
            serializer = MaintenanceRequestSerializer(maintenance_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

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

class SubmitComplaintView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tenantId):
        data = request.data
        try:
            tenant = Tenant.objects.get(id=tenantId)
            complaint = Complaint.objects.create(
                tenant=tenant,
                description=data['description'],
                priority_level=data['priority_level']
            )
            serializer = ComplaintSerializer(complaint)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenantId):
        notifications = Notification.objects.filter(tenant_id=tenantId)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def put(self, request, tenantId):
        notification = Notification.objects.get(id=request.data.get('id'), tenant_id=tenantId)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})
