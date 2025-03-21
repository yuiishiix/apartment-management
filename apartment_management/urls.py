from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),  # User authentication (registration)
    path('api/tenants/', include('tenants.urls')),  # Tenant profiles
    path('api/maintenance/', include('maintenance.urls')),  # Maintenance requests
    path('api/payments/', include('payments.urls')),  # Payments
    path('api/complains/', include('complains.urls')),  # Complaints
    path('api/notifications/', include('notifications.urls')),  # Notifications
    path('api/facility/', include('facility.urls')),  # Facility management
    path('api/polls/', include('polls.urls')),  # Polls
]

