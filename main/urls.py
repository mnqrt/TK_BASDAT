from django.urls import path
from main.views import *


urlpatterns = [
    path('',show_homepage, name="show_homepage")
]