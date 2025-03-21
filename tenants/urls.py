from django.urls import path
from .views import TenantProfileView, AllTenantsListView

urlpatterns = [
    path('<int:tenantId>/profile/', TenantProfileView.as_view(), name='tenant-profile'),
    path('tenants/', AllTenantsListView.as_view(), name='all-tenants-list'),  # Fetch all tenants

]
