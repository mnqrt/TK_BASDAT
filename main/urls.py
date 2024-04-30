from django.urls import path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('',show_homepage, name="show_homepage"),
    path('login/', login_page, name='login'),
    path('login/authenticate', authenticate_user, name='authenticate'), 
    path('logout/', logout, name='logout'),  
]