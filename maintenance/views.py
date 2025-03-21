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
