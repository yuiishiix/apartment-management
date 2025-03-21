# payments/urls.py
from django.urls import path
from .views import SubmitPaymentView, TenantPaymentsListView, PaymentReceiptView, AssessLateFeeView, \
    DeletePaymentMethodView

urlpatterns = [
    path('tenant/<int:tenantId>/pay-rent/', SubmitPaymentView.as_view(), name='submit-payment'),
    path('tenant/<int:tenantId>/payments/', TenantPaymentsListView.as_view(), name='tenant-payments'),
    path('receipt/<int:paymentId>/', PaymentReceiptView.as_view(), name='payment-receipt'),
    path('tenant/<str:apartment_number>/late-fee/assess/', AssessLateFeeView.as_view(), name='assess-late-fee'),
    path('payment/gateway/<int:payment_id>/', DeletePaymentMethodView.as_view(), name='delete-payment-method'),

]
