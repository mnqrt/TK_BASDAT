from django.urls import path
from . import views

app_name = 'album'

urlpatterns = [
    path('', views.album_views, name='album_views'),
    path('/', views.album_views, name='album_views'),
    path('create-lagu/<uuid:album_id>/', views.create_lagu, name='create_lagu'),
    path('daftar-lagu/<uuid:album_id>/', views.daftar_lagu, name='daftar_lagu'),
]