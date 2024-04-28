from django.urls import path
from playlist.views import *


urlpatterns = [
    path('', show_akun, name='show_akun'),
    path('show_song', show_song, name='show_song')
]