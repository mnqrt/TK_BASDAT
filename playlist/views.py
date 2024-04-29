from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_playlists_by_email(request, email):
    print(email)
    query_str = f"SELECT * FROM USER_PLAYLIST WHERE email_pembuat='{email}'"
    user_playlists = query(query_str)
    for user_playlist in user_playlists:
        user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')
    return render(request, 'index.html', {'playlists': user_playlists})

def show_playlist_by_id(request, id_user_playlist):
    print(id_user_playlist)

    try:
        query_str = f"SELECT * FROM USER_PLAYLIST WHERE id_user_playlist='{id_user_playlist}'"
        user_playlist = query(query_str)[0]
        user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')

        playlist_id = user_playlist["id_playlist"]
        email = user_playlist["email_pembuat"]

        query_str = f"""SELECT 
                            K.judul AS judul,
                            A.nama AS nama_artis,
                            K.durasi AS durasi
                        FROM PLAYLIST_SONG PS
                        JOIN SONG S ON S.id_konten=PS.id_song
                        JOIN KONTEN K ON K.id=S.id_konten
                        JOIN ARTIS AA ON AA.id=S.id_artist
                        JOIN AKUN A ON A.email=AA.email_akun
                        WHERE PS.id_playlist='{playlist_id}'"""
        songs = query(query_str)

        query_str = f"""SELECT nama FROM AKUN WHERE email='{email}'"""
        nama = query(query_str)[0]


        return render(request, 'detail.html', {'user_playlist': user_playlist, 'songs': songs, 'nama': nama})
    except:
        return render(request, 'failed.html')

# Create your views here.
def show_song(request):
    query_str = "SELECT * FROM konten"
    hasil = query(query_str)
    return render(request, 'konten.html', {'konten': hasil})

"""
SELECT 
    K.judul AS judul,
    A.nama AS nama_artis,
    K.durasi AS durasi
FROM PLAYLIST_SONG PS
JOIN SONG S ON S.id_konten=PS.id_song
JOIN KONTEN K ON K.id=S.id_konten
JOIN ARTIS AA ON AA.id=S.id_artist
JOIN AKUN A ON A.email=AA.email_akun
WHERE PS.id_playlist=playlist_id


SELECT 
    K.judul AS judul,
    A.nama AS nama_artis,
    K.durasi AS durasi
FROM PLAYLIST_SONG PS
JOIN SONG S ON S.id_konten=PS.id_song
JOIN KONTEN K ON K.id=S.id_konten
JOIN ARTIS AA ON AA.id=S.id_artist
JOIN AKUN A ON A.email=AA.email_akun
WHERE PS.id_playlist='a6a6d81f-1f14-427b-8409-cb9fe93d6963'
"""