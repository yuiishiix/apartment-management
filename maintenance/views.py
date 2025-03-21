from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MaintenanceRequest, Tenant
from .serializers import MaintenanceRequestSerializer

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

class LandlordMaintenanceRequestsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can view the requests

    def get(self, request):
        try:
            # Fetch all maintenance requests for all tenants
            maintenance_requests = MaintenanceRequest.objects.all()
            serializer = MaintenanceRequestSerializer(maintenance_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MaintenanceRequestStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can view the status

    def get(self, request, maintenanceId):
        try:
            # Fetch the maintenance request by its ID
            maintenance_request = MaintenanceRequest.objects.get(id=maintenanceId)

            # You could also return only the status if you want a smaller response
            return Response({"status": maintenance_request.status}, status=status.HTTP_200_OK)
        except MaintenanceRequest.DoesNotExist:
            return Response({"error": "Maintenance request not found"}, status=status.HTTP_404_NOT_FOUND)


class MaintenanceRequestPriorityView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can update the priority

    def patch(self, request, maintenanceId):
        data = request.data
        try:
            # Fetch the maintenance request by its ID
            maintenance_request = MaintenanceRequest.objects.get(id=maintenanceId)

            # Ensure the priority level is valid (you can add more validation logic if needed)
            new_priority = data.get("urgency_level", None)
            if new_priority not in ['low', 'medium', 'high']:
                return Response({"error": "Invalid priority level."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the priority level
            maintenance_request.urgency_level = new_priority
            maintenance_request.save()

            # Serialize the updated maintenance request
            serializer = MaintenanceRequestSerializer(maintenance_request)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except MaintenanceRequest.DoesNotExist:
            return Response({"error": "Maintenance request not found"}, status=status.HTTP_404_NOT_FOUND)