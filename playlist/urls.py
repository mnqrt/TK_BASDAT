from django.urls import path
from playlist.views import *


urlpatterns = [
    path('show_playlist_by_username/<str:email>', show_playlist_by_email, name='show_akun'),
    path('show_song', show_song, name='show_song')
]