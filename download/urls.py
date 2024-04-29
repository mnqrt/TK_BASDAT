from django.urls import path
from download.views import *

app_name = 'download'
urlpatterns = [
    path('', show_download, name='show_download'),
]