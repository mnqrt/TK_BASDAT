from django.urls import path

from podcast.views import podcast_detail

app_name = 'podcast'

urlpatterns = [
    path('podcast/<uuid:podcast_id>/', podcast_detail, name='podcast_detail'),
]
