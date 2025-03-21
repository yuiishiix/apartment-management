from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Facility, Booking
from .serializers import FacilitySerializer, BookingSerializer
from datetime import datetime


from datetime import datetime

from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Facility, Booking

class FacilityAvailabilityView(APIView):
    def get(self, request, facility_id):
        try:
            facility = Facility.objects.get(id=facility_id)
        except Facility.DoesNotExist:
            return Response({"detail": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get date, start_time, and end_time from request parameters
        date = request.query_params.get('date')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not date or not start_time or not end_time:
            return Response({"detail": "Date, start_time, and end_time are required"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received start_time: {start_time}, end_time: {end_time}")  # Debug log

        try:
            # Validate time format using strptime
            datetime.strptime(start_time, '%H:%M')  # Check start_time format
            datetime.strptime(end_time, '%H:%M')  # Check end_time format
        except ValueError:
            return Response({"detail": "Invalid time format. Please use 'HH:MM'."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if there are existing bookings for the requested date and time
        bookings = Booking.objects.filter(facility=facility, date=date)

        for booking in bookings:
            if not (end_time <= booking.start_time or start_time >= booking.end_time):
                return Response({"available": False, "detail": "Facility is already booked for the requested time."}, status=status.HTTP_200_OK)

        return Response({"available": True}, status=status.HTTP_200_OK)


class FacilityBookingView(APIView):
    def post(self, request, facility_id):
        try:
            facility = Facility.objects.get(id=facility_id)
        except Facility.DoesNotExist:
            return Response({"detail": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not date or not start_time or not end_time:
            return Response({"detail": "Date, start_time, and end_time are required"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received start_time: {start_time}, end_time: {end_time}")  # Debug log

        try:
            # Validate time format using strptime
            datetime.strptime(start_time, '%H:%M')  # Check start_time format
            datetime.strptime(end_time, '%H:%M')  # Check end_time format
        except ValueError:
            return Response({"detail": "Invalid time format. Please use 'HH:MM'."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the facility is available for the given time
        bookings = Booking.objects.filter(facility=facility, date=date)

        for booking in bookings:
            if not (end_time <= booking.start_time or start_time >= booking.end_time):
                return Response({"detail": "Facility is already booked for the requested time"}, status=status.HTTP_400_BAD_REQUEST)

        # If available, create a new booking
        tenant = request.user.tenant  # Assuming user is authenticated
        new_booking = Booking(facility=facility, tenant=tenant, date=date, start_time=start_time, end_time=end_time)
        new_booking.save()

        return Response({"detail": "Facility booked successfully"}, status=status.HTTP_201_CREATED)
