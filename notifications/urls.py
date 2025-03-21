from django.urls import path
from .views import NotificationsView, AnnouncementListCreateView, AllNotificationsView

urlpatterns = [
    path('notify/', NotificationsView.as_view(), name='notify-all-tenants'),
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('notifications/', AllNotificationsView.as_view(), name='all-notifications'),
    path('community/events/', AnnouncementListCreateView.as_view(), name='announcement-list-create'),

]
