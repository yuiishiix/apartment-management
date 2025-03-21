from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notification, Tenant, Announcement
from .serializers import NotificationSerializer, AnnouncementSerializer


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            # Fetching all tenants
            tenants = Tenant.objects.all()

            # Creating notifications for all tenants
            notifications = []
            for tenant in tenants:
                notification = Notification.objects.create(
                    tenant=tenant,
                    notification_type=data['notification_type'],
                    message_content=data['message_content']
                )
                notifications.append(notification)

            # Serializing the notifications data and returning response
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
class AnnouncementListCreateView(APIView):
    """
    List all announcements or create a new one.
    """

    def get(self, request):
        announcements = Announcement.objects.filter(is_active=True)  # Only active announcements
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new announcement
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllNotificationsView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AnnouncementListCreateView(APIView):
    """
    List all announcements.
    """

    def get(self, request):
        announcements = Announcement.objects.all()  # Fetch all announcements, active or not
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)