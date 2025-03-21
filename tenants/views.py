from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Tenant
from .serializers import TenantSerializer
from main.models import CustomUser


class TenantProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenantId):
        try:
            print(f"Fetching tenant with ID: {tenantId}")
            tenant = Tenant.objects.get(id=tenantId)
            serializer = TenantSerializer(tenant)
            print("Tenant found:", serializer.data)
            return Response(serializer.data)
        except Tenant.DoesNotExist:
            print("Tenant not found")
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, tenantId):
        try:
            print(f"Updating tenant with ID: {tenantId}")
            tenant = Tenant.objects.get(id=tenantId)
            serializer = TenantSerializer(tenant, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                print("Tenant updated successfully:", serializer.data)
                return Response(serializer.data)

            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tenant.DoesNotExist:
            print("Tenant not found")
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LandlordTenantListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, landlordId):
        try:
            landlord = CustomUser.objects.get(id=landlordId)
            tenants = Tenant.objects.filter(landlord=landlord)
            serializer = TenantSerializer(tenants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Landlord not found"}, status=status.HTTP_404_NOT_FOUND)