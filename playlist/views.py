from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_playlist_by_email(request, email):
    print(email)
    query_str = f"SELECT * FROM USER_PLAYLIST WHERE email_pembuat='{email}'"
    user_playlists = query(query_str)
    # print(user_playlists)
    for user_playlist in user_playlists:
        user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')
    return render(request, 'index.html', {'akun': user_playlists})

# Create your views here.
def show_song(request):
    query_str = "SELECT * FROM konten"
    hasil = query(query_str)
    return render(request, 'konten.html', {'konten': hasil})