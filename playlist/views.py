from http.client import HTTPResponse
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def show_playlists_by_email(request, email):
    query_str = f"SELECT * FROM USER_PLAYLIST WHERE email_pembuat='{email}'"
    user_playlists = query(query_str)
    for user_playlist in user_playlists:
        user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')
    return render(request, 'index.html', {'playlists': user_playlists})

def show_playlist_by_id(request, id_user_playlist):

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
    
def add_song_to_playlist_page(request, id_user_playlist):
    query_str = f"""
                SELECT
                    k.judul AS judul_lagu,
                    a.nama AS nama_artis,
                    s.id_konten AS id_lagu
                FROM SONG s
                JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten=sws.id_song
                JOIN SONGWRITER sw ON sws.id_songwriter=sw.id
                JOIN KONTEN k ON k.id=s.id_konten
                JOIN AKUN a ON a.email=sw.email_akun
                WHERE s.id_konten NOT in (
                    SELECT id_song
                    FROM PLAYLIST_SONG ps
                    JOIN USER_PLAYLIST up ON ps.id_playlist=up.id_playlist
                    WHERE up.id_user_playlist='{id_user_playlist}'
                )
                """
    songs_with_artist = query(query_str)
    return render(request, 'add-song.html', {'song_artist':songs_with_artist, 'id_user_playlist': id_user_playlist})

def add_song_to_playlist(request, id_user_playlist, id_song):
    try:
        query_str = f"SELECT id_playlist FROM USER_PLAYLIST WHERE id_user_playlist='{id_user_playlist}'"
        id_playlist = query(query_str)[0]['id_playlist']
        query_str = f"INSERT INTO PLAYLIST_SONG (id_playlist, id_song) VALUES('{id_playlist}', '{id_song}')"
        add_song_res = query(query_str)
        return HTTPResponse("Song added to playlist successfully!")
    except:
        return render(request, 'failed.html')

def play_song_page(request, email, id_song):
    query_str = f"""SELECT k.judul AS judul 
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='{id_song}'"""
    judul = query(query_str)[0]['judul']

    query_str = f"""SELECT g.genre AS genre 
                    FROM SONG s JOIN KONTEN k ON k.id=s.id_konten 
                    JOIN GENRE g ON g.id_konten=k.id 
                    WHERE g.id_konten='{id_song}'"""
    genre = query(query_str)[0]['genre']

    query_str = f"""SELECT a.nama AS nama_artis
                    FROM SONG s
                    JOIN KONTEN k ON k.id=s.id_konten 
                    JOIN ARTIS ar ON ar.id=s.id_artist
                    JOIN AKUN a ON a.email=ar.email_akun
                    WHERE s.id_konten='{id_song}'"""
    res = query(query_str)
    nama_artis = res[0]['nama_artis'] if len(res) > 0 else None

    query_str = f"""SELECT a.nama AS nama_songwriter
                    FROM SONG s
                    JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten=sws.id_song
                    JOIN SONGWRITER sw ON sws.id_songwriter=sw.id
                    JOIN AKUN a ON a.email=sw.email_akun
                    WHERE s.id_konten='{id_song}'"""
    res = query(query_str)
    nama_songwriter = ", ".join([obj_songwriter['nama_songwriter'] for  obj_songwriter in res])


    query_str = f"""SELECT k.durasi AS durasi
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='{id_song}'"""
    durasi = query(query_str)[0]['durasi']

    query_str = f"""SELECT k.tanggal_rilis AS tanggal_rilis
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='{id_song}'"""
    tanggal_rilis = query(query_str)[0]['tanggal_rilis']

    query_str = f"""SELECT k.tahun AS tahun
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='{id_song}'"""
    tahun = query(query_str)[0]['tahun']

    query_str = f"""SELECT COUNT(aps.email_pemain) AS total_play
                    FROM SONG s
                    LEFT JOIN AKUN_PLAY_SONG aps ON s.id_konten=aps.id_song
                    WHERE s.id_konten='{id_song}'
                    GROUP BY s.id_konten"""
    total_play = query(query_str)[0]['total_play']

    query_str = f"""SELECT COUNT(*) AS total_download
                    FROM SONG s
                    LEFT JOIN DOWNLOADED_SONG ds ON ds.id_song=s.id_konten
                    WHERE s.id_konten='{id_song}'
                    GROUP BY s.id_konten"""
    res = query(query_str)
    total_download = res[0]['total_download'] if len(res) > 0 else None

    query_str = f"""SELECT a.judul AS album
                    FROM SONG s
                    JOIN ALBUM a ON s.id_album=a.id
                    WHERE s.id_konten='{id_song}'"""
    album = query(query_str)[0]['album']

    return render(request, 'play-song.html', {'judul':judul,'genre':genre,'nama_artis':nama_artis,'nama_songwriter':nama_songwriter,
                                            'durasi':durasi,'tanggal_rilis':tanggal_rilis,'tahun':tahun,
                                            'total_play':total_play,'total_download':total_download,'album':album,
                                            'email':email, 'id_song':id_song})

def play_song(request, email, id_song):
    try:
        query_str = f"INSERT INTO TABLE (email_pemain, id_song) VALUES ('{email}', '{id_song}')"
        res = query(query_str)
        return HTTPResponse("Song added to playlist successfully!")
    except:
        return render(request, 'failed.html')

def add_song_to_any_playlist_page(request, email, id_song):
    query_str = f"""SELECT k.judul AS judul, a.nama AS nama_artis 
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    JOIN ARTIS ar ON ar.id=s.id_artist
                    JOIN AKUN a ON a.email=ar.email_akun
                    WHERE s.id_konten='{id_song}'"""
    judul_artis = query(query_str)[0]
    judul, artis = judul_artis['judul'], judul_artis['nama_artis']

    query_str = f"""SELECT * FROM USER_PLAYLIST up WHERE up.email_pembuat='{email}' AND
                    '{id_song}' NOT IN (
                        SELECT ps.id_song
                        FROM PLAYLIST_SONG ps 
                        WHERE ps.id_playlist=up.id_playlist
                    )"""
    user_playlists = query(query_str)
    print("--->",user_playlists)
    for user_playlist in user_playlists:
        user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')

    return render(request, 'add-song-any-playlist.html', {'judul': judul, 'artis': artis, 'playlists': user_playlists, 'id_song': id_song, 'email': email})

def download_song_page(request, email, id_song):
    query_str = f"""SELECT k.judul AS judul 
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='{id_song}'"""
    judul = query(query_str)[0]['judul']

    query_str = f"INSERT INTO DOWNLOADED_SONG(id_song, email_downloader) VALUES ('{id_song}', '{email}')"
    res = query(query_str)

    print(res)
    return render(request, "down-song.html", {'email':email, 'id_song':id_song, 'judul': judul})



# Create your views here.
def show_song(request):
    query_str = "SELECT * FROM konten"
    hasil = query(query_str)
    return render(request, 'konten.html', {'konten': hasil})

"""
SELECT
    k.judul AS judul_lagu,
    a.nama AS nama_artis
FROM SONG s
JOIN SONGWRITER_WRITE_SONG sws ON s.id_konten=sws.id_song
JOIN SONGWRITER sw ON sws.id_songwriter=sw.id
JOIN KONTEN k ON k.id=s.id_konten
JOIN AKUN a ON a.email=sw.email_akun

SELECT COUNT(*) AS total_download
                    FROM SONG s
                    LEFT JOIN DOWNLOADED_SONG ds ON ds.id_song=s.id_konten
                    GROUP BY s.id_konten
                    WHERE s.id_konten='b8e409f4-89b9-4914-99e2-743c6411c8fb'


                    v

                    SELECT k.judul AS judul 
                    FROM SONG s 
                    JOIN KONTEN k ON k.id=s.id_konten 
                    WHERE s.id_konten='b8e409f4-89b9-4914-99e2-743c6411c8fb'
"""