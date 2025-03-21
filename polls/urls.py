from django.urls import path
from . import views

urlpatterns = [
    path('polls/', views.PollListView.as_view(), name='poll-list'),
    path('polls/<int:pk>/vote/', views.VotePollView.as_view(), name='poll-vote'),
]
