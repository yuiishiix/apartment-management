from .models import Tenant, MaintenanceRequest, Payment, Complaint, Notification
from .serializers import TenantSerializer, MaintenanceRequestSerializer, PaymentSerializer, ComplaintSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'access': str(access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error during user registration:", str(e))
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Serializer errors:", serializer.errors)  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        try:
            notifications = Notification.objects.filter(tenant_id=tenantId)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response({"error": "Notifications not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, tenantId):
        try:
            notification = Notification.objects.get(id=request.data.get('id'), tenant_id=tenantId)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read"})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found or you don't have permission to update this notification."},
                            status=status.HTTP_404_NOT_FOUND)
