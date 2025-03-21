from django.urls import path
from .views import NotificationsView

urlpatterns = [
    path('<int:tenantId>/', NotificationsView.as_view(), name='notifications'),
]
