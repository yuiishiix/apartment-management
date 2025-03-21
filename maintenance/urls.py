from django.urls import path
from .views import SubmitMaintenanceRequestView, LandlordMaintenanceRequestsView, MaintenanceRequestStatusView, \
    MaintenanceRequestPriorityView

urlpatterns = [
    path('<int:tenantId>/submit/', SubmitMaintenanceRequestView.as_view(), name='submit-maintenance'),
    path('maintenance-requests/', LandlordMaintenanceRequestsView.as_view(), name='maintenance-requests'),
    path('<int:maintenanceId>/status/', MaintenanceRequestStatusView.as_view(), name='maintenance-status'),
    path('<int:maintenanceId>/priority/', MaintenanceRequestPriorityView.as_view(), name='maintenance-priority'),

]
