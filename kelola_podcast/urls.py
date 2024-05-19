from django.urls import path
from . import views

urlpatterns = [
    path('create_podcast/', views.create_podcast, name='create_podcast'),
    path('list_podcast/', views.list_podcast, name='list_podcast'),
    path('create_episode/<uuid:podcast_id>/', views.create_episode, name='create_episode'),
    path('delete_podcast/<uuid:podcast_id>/', views.delete_podcast, name='delete_podcast'),
    path('list_episodes/<uuid:podcast_id>/', views.list_episodes, name='list_episodes'),
    path('delete_episode/<uuid:episode_id>/', views.delete_episode, name='delete_episode'),
]
