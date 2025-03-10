from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView  # Import the RegisterView
from . import views

urlpatterns = [
    path('tenant/<int:tenantId>/profile/', views.TenantProfileView.as_view(), name='tenant-profile'),
    path('tenant/<int:tenantId>/maintenance/submit/', views.SubmitMaintenanceRequestView.as_view(), name='submit-maintenance'),
    path('tenant/<int:tenantId>/pay-rent/', views.SubmitPaymentView.as_view(), name='pay-rent'),
    path('tenant/<int:tenantId>/complaints/submit/', views.SubmitComplaintView.as_view(), name='submit-complaint'),
    path('tenant/<int:tenantId>/notifications/', views.NotificationsView.as_view(), name='notifications'),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

]
