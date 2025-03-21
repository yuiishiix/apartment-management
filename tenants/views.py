from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Tenant
from .serializers import TenantSerializer

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
