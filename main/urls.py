from django.urls import path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('',show_homepage, name="show_homepage"),
    path('login/', login_page, name='login'),
    path('login/authenticate', authenticate_user, name='authenticate'), 
    path('logout/', logout, name='logout'),
    path('search/', search, name='search'),  
    path('register/', register_page, name='register'),
    path('register-label/', register_label_page, name='register-label'),
    path('reg-label/', register_label, name='reg-label'),
    path('register-pengguna/', register_pengguna_page, name='register-pengguna'),
    path('reg-pengguna/', register_pengguna, name='reg-pengguna')
]