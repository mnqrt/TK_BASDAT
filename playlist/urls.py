from django.urls import path
from playlist.views import *


urlpatterns = [
    path('show-all-by-username/<str:email>', show_playlists_by_email, name='show_playlists_from_akun'),
    path('show-one-by-id/<str:id_user_playlist>', show_playlist_by_id, name='show_playlist_from_id'),
    path('add-song-page/<str:id_user_playlist>', add_song_to_playlist_page, name='add_song_to_playlist_page'),
    path('add-song/<str:id_user_playlist>/<str:id_song>', add_song_to_playlist, name='add_song_to_playlist'),
    path('play-song-page/<str:email>/<str:id_song>', play_song_page, name='play_song_page'),
    path('show_song', show_song, name='show_song')
]