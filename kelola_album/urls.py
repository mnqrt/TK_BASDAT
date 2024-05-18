from django.urls import path
from kelola_album.views import *

app_name = 'kelola_album'

urlpatterns = [
    path('create-album/', create_album, name='create_album'),
    path('create-lagu/', create_lagu, name='create_lagu'),
    path('list-album/', list_album, name='list_album'),
    path('list-album-edit/', list_album_edit, name='list_album_edit'),
    path('list-song/', list_song, name='list_song'),
    path('delete_album/', delete_album, name='delete_album'),
    path('delete_lagu/', delete_lagu, name='delete_lagu')
]