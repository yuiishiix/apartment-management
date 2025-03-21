from django.urls import path
from .views import TenantProfileView

urlpatterns = [
    path('<int:tenantId>/profile/', TenantProfileView.as_view(), name='tenant-profile'),
]
