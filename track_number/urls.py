from django.urls import path
from .api_client import TrackNumberAPIView

urlpatterns = [
    path('api/track/<str:track_number>/', TrackNumberAPIView.as_view(),
         name='track-number-api'),
    path('api/track/hui', TrackNumberAPIView.as_view(),
         name='create-task-in-amo')
]
