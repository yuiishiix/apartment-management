from django.urls import path
from .views import SubmitPaymentView

urlpatterns = [
    path('<int:tenantId>/submit/', SubmitPaymentView.as_view(), name='submit-payment'),
]
