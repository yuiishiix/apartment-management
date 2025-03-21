from django.urls import path
from .views import FacilityAvailabilityView, FacilityBookingView

urlpatterns = [
    path('facility/<int:facility_id>/availability/', FacilityAvailabilityView.as_view(), name='facility-availability'),
    path('facility/<int:facility_id>/book/', FacilityBookingView.as_view(), name='facility-booking'),
]
