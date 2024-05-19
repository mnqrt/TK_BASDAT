from django.urls import path
from podcast.views import play_podcast

app_name = 'play_podcast'

urlpatterns = [
    path('podcast/<uuid:id_podcast>/', play_podcast, name='play_podcast')
]