from django.urls import path
from playlist.views import *


urlpatterns = [
    path('show-all-by-username/<str:email>', show_playlists_by_email, name='show_playlists_from_akun'),
    path('show-one-by-id/<str:id_user_playlist>', show_playlist_by_id, name='show_playlist_from_id'),
    path('add-song-page/<str:id_user_playlist>', add_song_to_playlist_page, name='add_song_to_playlist_page'),
    path('add-song/<str:id_user_playlist>/<str:id_song>', add_song_to_playlist, name='add_song_to_playlist'),
    path('delete-song/<str:id_user_playlist>/<str:id_song>', delete_song_from_playlist, name='delete_from_playlist'),
    path('add-song-to-any-playlist-page/<str:email>/<str:id_song>', add_song_to_any_playlist_page, name='add_song_to_any_playlist'),
    path('play-song-page/<str:email>/<str:id_song>', play_song_page, name='play_song_page'),
    path('play-song/<str:email>/<str:id_song>', play_song, name='play_song'),
    path('down-song-page/<str:email>/<str:id_song>', download_song_page, name='download_song_page'),
    path('add-playlist/<str:email>/<str:judul>/<str:deskripsi>', add_playlist, name='add_playlist'),
    path('delete-playlist/<str:id_user_playlist>', delete_playlist, name='delete_playlist'),
    path('update-playlist/<str:id_user_playlist>/<str:title>/<str:description>', update_playlist, name='update_playlist'),
    path('akun-play-user-playlist/<str:email>/<str:id_user_playlist>', akun_play_user_playlist, name='akun_play_user_playlist'),
    path('show_song', show_song, name='show_song')
]