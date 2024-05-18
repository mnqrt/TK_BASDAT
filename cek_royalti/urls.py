from django.urls import path
from cek_royalti.views import *

app_name = 'cek_royalti'

urlpatterns = [
    path('cek_royalti/', cek_royalti, name='cek_royalti')
]