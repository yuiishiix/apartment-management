from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Complaint, Tenant
from .serializers import ComplaintSerializer

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
