from django.urls import path
from .views import SubmitMaintenanceRequestView

urlpatterns = [
    path('<int:tenantId>/submit/', SubmitMaintenanceRequestView.as_view(), name='submit-maintenance'),
]
