from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tenantId):
        notifications = Notification.objects.filter(tenant_id=tenantId)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def put(self, request, tenantId):
        try:
            notification = Notification.objects.get(id=request.data.get('id'), tenant_id=tenantId)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read"})
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
