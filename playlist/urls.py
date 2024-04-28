from django.urls import path
from playlist.views import *


urlpatterns = [
    path('show-all-by-username/<str:email>', show_playlists_by_email, name='show_playlists_from_akun'),
    path('show-one-by-id/<str:id_user_playlist>', show_playlist_by_id, name='show_playlist_from_id'),
    path('show_song', show_song, name='show_song')
]