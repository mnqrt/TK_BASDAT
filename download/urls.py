from django.urls import path
from download.views import *

app_name = 'download'
urlpatterns = [
    path('', show_download, name='show_download'),
    path('by/<str:email>/', show_download_by_email, name='by_email'),  
    path('delete', delete_download, name='delete'),  
]