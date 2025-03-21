from django.urls import path
from .views import SubmitComplaintView

urlpatterns = [
    path('<int:tenantId>/complain/submit/', SubmitComplaintView.as_view(), name='submit-complaint'),
]
