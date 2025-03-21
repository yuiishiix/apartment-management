from django.urls import path
from .views import TenantProfileView

urlpatterns = [
    path('<int:tenantId>/', TenantProfileView.as_view(), name='tenant-profile'),
]
