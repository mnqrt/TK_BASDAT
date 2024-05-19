import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime

def create_album(request):
    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('judul')
        label = request.POST.get('label')
        id_album = str(uuid.uuid4())
        query(
            f'insert into album values (\'{id_album}\', \'{judul}\', 0, \'{label}\', 0)')
        
        connection.commit()
        return redirect('album_royalti:list_edit_album')
    
    query(
        f'select id, nama from label')
    list_label = cursor.fetchall()
    context = {
        'list_label': list_label
    }
    return render(request, 'create_album.html', context)


def create_song(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    idArtist = request.COOKIES.get('idArtist')
    idSongwriter = request.COOKIES.get('idSongwriter')
    album_id = request.GET.get('album_id')
    nama_artist = ""
    nama_songwriter = ""

    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('judul')
        id_song = str(uuid.uuid4())
        durasi = request.POST.get('durasi')
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year
        year_now = '{:04d}'.format(current_year)
        songwriters = request.POST.getlist('songwriter[]')
        genres = request.POST.getlist('genre[]')

        if isArtist == "True":
            id_artist = idArtist
            id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
        else:
            id_artist = request.POST.get('artist')
            query(
                f'select id_pemilik_hak_cipta from artist where id = \'{id_artist}\'')
            id_pemilik_hak_cipta_artist = cursor.fetchone()

        # insert ke tabel konten
        query(
            f'insert into konten values (\'{id_song}\', \'{judul}\', \'{date_now}\', \'{year_now}\', \'{durasi}\')')
        
        # insert ke tabel song
        query(
            f'insert into song values (\'{id_song}\', \'{id_artist}\', \'{album_id}\', 0, 0)')
        
        # insert ke songwriter_write_song dan royalti
        for songwriter in songwriters:
            query(
                f'select id_pemilik_hak_cipta from songwriter where id = \'{songwriter}\'')
            id_pemilik_hak_cipta_songwriter = cursor.fetchone();
            query(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_songwriter[0]}\', \'{id_song}\', 0)')
            query(
                f'insert into songwriter_write_song values (\'{songwriter}\', \'{id_song}\')')

        # insert ke genre
        for genre in genres:
            query(
                f'insert into genre values (\'{id_song}\', \'{genre}\')')
        
        # insert royalti artist
        query(
            f'insert into royalti values (\'{id_pemilik_hak_cipta_artist[0]}\', \'{id_song}\', 0)')
        
        # insert royalti label
        query(
            f'select id_label from album where id = \'{album_id}\'')
        id_label = cursor.fetchone()
        query(
            f'select id_pemilik_hak_cipta from label where id = \'{id_label[0]}\'')
        id_pemilik_hak_cipta_label = cursor.fetchone()
        query(
            f'insert into royalti values (\'{id_pemilik_hak_cipta_label[0]}\', \'{id_song}\', 0)')
        
        # update album
        query(
            f'select jumlah_lagu, total_durasi from album where id = \'{album_id}\'')
        album_saat_ini = cursor.fetchone()
        new_total_durasi = int(album_saat_ini[1]) + int(durasi)
        new_jumlah_lagu = int(album_saat_ini[0]) + 1
        query(
            f'UPDATE album SET jumlah_lagu = {new_jumlah_lagu}, total_durasi = {new_total_durasi} WHERE id = \'{album_id}\'')
        
        connection.commit()
        return redirect('album_royalti:list_edit_album')

    # untuk pilihan dropdown artist
    query(
        f'select id, email_akun, id_pemilik_hak_cipta from artist')
    records_artist = cursor.fetchall()
    for i in range(len(records_artist)):
        query(
            f'select nama from akun where email = \'{records_artist[i][1]}\'')
        records_artist[i] = records_artist[i] + cursor.fetchone()

    # untuk pilihan dropdown songwriter
    query(
        f'select id, email_akun, id_pemilik_hak_cipta from songwriter')
    records_songwriter = cursor.fetchall()
    for i in range(len(records_songwriter)):
        query(
            f'select nama from akun where email = \'{records_songwriter[i][1]}\'')
        records_songwriter[i] = records_songwriter[i] + cursor.fetchone()

    # untuk pilihan dropdown genre
    query(
        f'select distinct genre from genre')
    records_genre = cursor.fetchall()

    # get nama album
    query(
        f'select judul from album where id = \'{album_id}\'')
    judul_album = cursor.fetchone()

    # get nama artist
    if isArtist == "True":
        query(
            f'select email_akun from artist where id = \'{idArtist}\'')
        email_artist = cursor.fetchone()
        query(
            f'select nama from akun where email = \'{email_artist[0]}\'')
        nama_artist = cursor.fetchone()

    # get nama songwriter
    if isSongwriter == "True":
        query(
            f'select email_akun from songwriter where id = \'{idSongwriter}\'')
        email_songwriter = cursor.fetchone()
        query(
            f'select nama from akun where email = \'{email_songwriter[0]}\'')
        nama_songwriter = cursor.fetchone()

    context = {
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'idArtist': idArtist,
        'idSongwriter': idSongwriter,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'judul_album': judul_album,
        'nama_artist': nama_artist,
        'nama_songwriter': nama_songwriter,
    }
    return render(request, 'create_song.html', context)


def list_album(request):
    email = request.COOKIES.get('email')

    query(
        f'select * from label where email = \'{email}\'')
    label = cursor.fetchmany()
    if len(label) == 1:
        # Cari album yang dimiliki label
        id_label = label[0][0]
        query(
            f'select * from album where id_label = \'{id_label}\'')
        records_album = cursor.fetchall()
        context = {
            'role': 'label',
            'status': 'success',
            'id': label[0][0],
            'nama': label[0][1],
            'email': label[0][2],
            'kontak': label[0][4],
            'id_pemilik_hak_cipta': label[0][5],
            'records_album': records_album,
        }
        response = render(request, 'list_album.html', context)
        response.set_cookie('role', 'label')
        response.set_cookie('email', email)
        response.set_cookie('id', label[0][0])
        response.set_cookie('idPemilikCiptaLabel', label[0][5])
        return response
    return render(request, 'list_album.html')


def list_edit_album(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    records_album_artist = []
    records_album_songwriter = []
    artistHasAlbum = False
    songwriterHasAlbum = False

    # kalau dia artist, list album dia sebagai artist
    if isArtist == "True" :
        id_artist = request.COOKIES.get('idArtist')
        list_album_id_artist = []
        query(
            f'SELECT DISTINCT id_album FROM SONG WHERE id_artist = \'{id_artist}\'')
        list_album_id_artist = cursor.fetchall()

        if len(list_album_id_artist) != 0:
            artistHasAlbum = True
            for id_album in list_album_id_artist:
                query(
                    f'SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album[0]}\'')
                records_album_artist.append(cursor.fetchone())
            for i in range(len(records_album_artist)):
                query(
                    f'SELECT nama FROM LABEL WHERE id = \'{records_album_artist[i][2]}\'')
                records_album_artist[i] = records_album_artist[i] + cursor.fetchone() 

    # kalau dia songwriter, list album dia sebagai songwriter
    if isSongwriter == "True":
        id_songwriter = request.COOKIES.get('idSongwriter')
        list_song_id_songwriter = []
        query(
            f'SELECT id_song FROM songwriter_write_song WHERE id_songwriter =  \'{id_songwriter}\'')
        list_song_id_songwriter = cursor.fetchall()

        if len(list_song_id_songwriter) != 0:
            list_album_id_songwriter = []
            for song in list_song_id_songwriter:
                query(
                    f'SELECT id_album FROM SONG WHERE id_konten = \'{song[0]}\'')
                list_album_id_songwriter.append(cursor.fetchone())

            if len(list_album_id_songwriter) != 0:
                songwriterHasAlbum = True
                for id_album in list_album_id_songwriter:
                    query(
                        f'SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album[0]}\'')
                    records_album_songwriter.append(cursor.fetchone())
                for i in range(len(records_album_songwriter)):
                    query(
                        f'SELECT nama FROM LABEL WHERE id = \'{records_album_songwriter[i][2]}\'')
                    records_album_songwriter[i] = records_album_songwriter[i] + cursor.fetchone() 
        
    context = {
        'status': 'success',
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'artistHasAlbum': artistHasAlbum,
        'songwriterHasAlbum': songwriterHasAlbum,
        'records_album_artist': records_album_artist,
        'records_album_songwriter': records_album_songwriter,
    }
    response = render(request, 'list_edit_album.html', context)
    return response


def list_song(request):
    album_id = request.GET.get('album_id')
    records_song = []

    query(
        f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    records_song = cursor.fetchall()
    for i in range(len(records_song)):
        query(
            f'SELECT judul, tanggal_rilis, tahun, durasi from konten where id = \'{records_song[i][0]}\'')
        records_song[i] = records_song[i] + cursor.fetchone()

    context = {
        'status': 'success',
        'records_song': records_song,
    }
    response = render(request, 'list_song.html', context)
    return response

def delete_song(request):
    # id_song = request.GET.get('song_id')
    # query(
    #     f'delete from song where id_konten = \'{id_song}\'')
    return render(request, 'list_song.html')


# import uuid
# from django.shortcuts import redirect, render
# from utils.query import *
# from datetime import datetime

# def create_album(request):
#     if request.method == 'POST':
#         judul = request.POST.get('judul')
#         label = request.POST.get('label')
#         id_album = str(uuid.uuid4())
#         query(f'insert into album values (\'{id_album}\', \'{judul}\', 0, \'{label}\', 0)')
#         connection.commit()
#         return redirect('album_royalti:list_edit_album')
    
#     query(f'select id, nama from label')
#     list_label = cursor.fetchall()
#     context = {'list_label': list_label}
#     return render(request, 'create_album.html', context)

# def create_song(request):
#     isArtist = request.COOKIES.get('isArtist')
#     isSongwriter = request.COOKIES.get('isSongwriter')
#     idArtist = request.COOKIES.get('idArtist')
#     idSongwriter = request.COOKIES.get('idSongwriter')
#     album_id = request.GET.get('album_id')
#     nama_artist = ""
#     nama_songwriter = ""

#     if request.method == 'POST':
#         judul = request.POST.get('judul')
#         id_song = str(uuid.uuid4())
#         durasi = request.POST.get('durasi')
#         current_datetime = datetime.now()
#         date_now = current_datetime.strftime('%Y-%m-%d')
#         current_year = current_datetime.year
#         year_now = '{:04d}'.format(current_year)
#         songwriters = request.POST.getlist('songwriter[]')
#         genres = request.POST.getlist('genre[]')

#         id_artist, id_pemilik_hak_cipta_artist = get_artist_details(isArtist, idArtist)

#         insert_konten(id_song, judul, date_now, year_now, durasi)
#         insert_song(id_song, id_artist, album_id)
#         insert_songwriter_write_song(id_song, songwriters)
#         insert_genres(id_song, genres)
#         insert_royalti(id_pemilik_hak_cipta_artist, id_song)
#         insert_royalti_label(album_id, id_song)
#         update_album(album_id, durasi)

#         connection.commit()
#         return redirect('album_royalti:list_edit_album')

#     records_artist = get_artist_records()
#     records_songwriter = get_songwriter_records()
#     records_genre = get_genre_records()
#     judul_album = get_album_title(album_id)
#     nama_artist = get_artist_name(isArtist, idArtist)
#     nama_songwriter = get_songwriter_name(isSongwriter, idSongwriter)

#     context = {
#         'isArtist': isArtist,
#         'isSongwriter': isSongwriter,
#         'idArtist': idArtist,
#         'idSongwriter': idSongwriter,
#         'records_artist': records_artist,
#         'records_songwriter': records_songwriter,
#         'records_genre': records_genre,
#         'judul_album': judul_album,
#         'nama_artist': nama_artist,
#         'nama_songwriter': nama_songwriter,
#     }
#     return render(request, 'create_song.html', context)

# def list_album(request):
#     email = request.COOKIES.get('email')
#     label = get_label_by_email(email)

#     if label:
#         id_label = label[0]
#         records_album = get_albums_by_label(id_label)
#         context = {
#             'role': 'label',
#             'status': 'success',
#             'id': label[0],
#             'nama': label[1],
#             'email': label[2],
#             'kontak': label[4],
#             'id_pemilik_hak_cipta': label[5],
#             'records_album': records_album,
#         }
#         response = render(request, 'list_album.html', context)
#         set_label_cookies(response, label)
#         return response

#     return render(request, 'list_album.html')

# def list_edit_album(request):
#     isArtist = request.COOKIES.get('isArtist')
#     isSongwriter = request.COOKIES.get('isSongwriter')
#     records_album_artist = []
#     records_album_songwriter = []
#     artistHasAlbum = False
#     songwriterHasAlbum = False

#     if isArtist == "True":
#         id_artist = request.COOKIES.get('idArtist')
#         list_album_id_artist = get_album_ids_by_artist(id_artist)

#         if list_album_id_artist:
#             artistHasAlbum = True
#             records_album_artist = get_album_records_by_ids(list_album_id_artist)

#     if isSongwriter == "True":
#         id_songwriter = request.COOKIES.get('idSongwriter')
#         list_album_id_songwriter = get_album_ids_by_songwriter(id_songwriter)

#         if list_album_id_songwriter:
#             songwriterHasAlbum = True
#             records_album_songwriter = get_album_records_by_ids(list_album_id_songwriter)

#     context = {
#         'status': 'success',
#         'isArtist': isArtist,
#         'isSongwriter': isSongwriter,
#         'artistHasAlbum': artistHasAlbum,
#         'songwriterHasAlbum': songwriterHasAlbum,
#         'records_album_artist': records_album_artist,
#         'records_album_songwriter': records_album_songwriter,
#     }
#     response = render(request, 'list_edit_album.html', context)
#     return response

# def list_song(request):
#     album_id = request.GET.get('album_id')
#     records_song = get_song_records_by_album(album_id)

#     context = {
#         'status': 'success',
#         'records_song': records_song,
#     }
#     response = render(request, 'list_song.html', context)
#     return response

# def delete_song(request):
#     return render(request, 'list_song.html')

# def get_artist_details(isArtist, idArtist):
#     if isArtist == "True":
#         id_artist = idArtist
#         id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
#     else:
#         id_artist = request.POST.get('artist')
#         query(f'select id_pemilik_hak_cipta from artist where id = \'{id_artist}\'')
#         id_pemilik_hak_cipta_artist = cursor.fetchone()
#     return id_artist, id_pemilik_hak_cipta_artist

# def insert_konten(id_song, judul, date_now, year_now, durasi):
#     query(f'insert into konten values (\'{id_song}\', \'{judul}\', \'{date_now}\', \'{year_now}\', \'{durasi}\')')

# def insert_song(id_song, id_artist, album_id):
#     query(f'insert into song values (\'{id_song}\', \'{id_artist}\', \'{album_id}\', 0, 0)')

# def insert_songwriter_write_song(id_song, songwriters):
#     for songwriter in songwriters:
#         query(f'select id_pemilik_hak_cipta from songwriter where id = \'{songwriter}\'')
#         id_pemilik_hak_cipta_songwriter = cursor.fetchone()
#         query(f'insert into royalti values (\'{id_pemilik_hak_cipta_songwriter[0]}\', \'{id_song}\', 0)')
#         query(f'insert into songwriter_write_song values (\'{songwriter}\', \'{id_song}\')')

# def insert_genres(id_song, genres):
#     for genre in genres:
#         query(f'insert into genre values (\'{id_song}\', \'{genre}\')')

# def insert_royalti(id_pemilik_hak_cipta, id_song):
#     query(f'insert into royalti values (\'{id_pemilik_hak_cipta}\', \'{id_song}\', 0)')

# def insert_royalti_label(album_id, id_song):
#     query(f'select id_label from album where id = \'{album_id}\'')
#     id_label = cursor.fetchone()
#     query(f'select id_pemilik_hak_cipta from label where id = \'{id_label[0]}\'')
#     id_pemilik_hak_cipta_label = cursor.fetchone()
#     query(f'insert into royalti values (\'{id_pemilik_hak_cipta_label[0]}\', \'{id_song}\', 0)')

# def update_album(album_id, durasi):
#     query(f'select jumlah_lagu, total_durasi from album where id = \'{album_id}\'')
#     album_saat_ini = cursor.fetchone()
#     new_total_durasi = int(album_saat_ini[1]) + int(durasi)
#     new_jumlah_lagu = int(album_saat_ini[0]) + 1
#     query(f'UPDATE album SET jumlah_lagu = {new_jumlah_lagu}, total_durasi = {new_total_durasi} WHERE id = \'{album_id}\'')

# def get_artist_records():
#     query(f'select id, email_akun, id_pemilik_hak_cipta from artist')
#     records_artist = cursor.fetchall()
#     for i in range(len(records_artist)):
#         query(f'select nama from akun where email = \'{records_artist[i][1]}\'')
#         records_artist[i] = records_artist[i] + cursor.fetchone()
#     return records_artist

# def get_songwriter_records():
#     query(f'select id, email_akun, id_pemilik_hak_cipta from songwriter')
#     records_songwriter = cursor.fetchall()
#     for i in range(len(records_songwriter)):
#         query(f'select nama from akun where email = \'{records_songwriter[i][1]}\'')
#         records_songwriter[i] = records_songwriter[i] + cursor.fetchone()
#     return records_songwriter

# def get_genre_records():
#     query(f'select distinct genre from genre')
#     records_genre = cursor.fetchall()
#     return records_genre

# def get_album_title(album_id):
#     query(f'select judul from album where id = \'{album_id}\'')
#     judul_album = cursor.fetchone()
#     return judul_album

# def get_artist_name(isArtist, idArtist):
#     nama_artist = ""
#     if isArtist == "True":
#         query(f'select email_akun from artist where id = \'{idArtist}\'')
#         email_artist = cursor.fetchone()
#         query(f'select nama from akun where email = \'{email_artist[0]}\'')
#         nama_artist = cursor.fetchone()
#     return nama_artist

# def get_songwriter_name(isSongwriter, idSongwriter):
#     nama_songwriter = ""
#     if isSongwriter == "True":
#         query(f'select email_akun from songwriter where id = \'{idSongwriter}\'')
#         email_songwriter = cursor.fetchone()
#         query(f'select nama from akun where email = \'{email_songwriter[0]}\'')
#         nama_songwriter = cursor.fetchone()
#     return nama_songwriter

# def get_label_by_email(email):
#     query(f'select * from label where email = \'{email}\'')
#     label = cursor.fetchmany()
#     return label[0] if label else None

# def get_albums_by_label(id_label):
#     query(f'select * from album where id_label = \'{id_label}\'')
#     records_album = cursor.fetchall()
#     return records_album

# def set_label_cookies(response, label):
#     response.set_cookie('role', 'label')
#     response.set_cookie('email', label[2])
#     response.set_cookie('id', label[0])
#     response.set_cookie('idPemilikCiptaLabel', label[5])

# def get_album_ids_by_artist(id_artist):
#     query(f'SELECT DISTINCT id_album FROM SONG WHERE id_artist = \'{id_artist}\'')
#     list_album_id_artist = cursor.fetchall()
#     return list_album_id_artist

# def get_album_records_by_ids(list_album_ids):
#     records_album = []
#     for id_album in list_album_ids:
#         query(f'SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album[0]}\'')
#         album_record = cursor.fetchone()
#         query(f'SELECT nama FROM LABEL WHERE id = \'{album_record[2]}\'')
#         album_record = album_record + cursor.fetchone()
#         records_album.append(album_record)
#     return records_album

# def get_album_ids_by_songwriter(id_songwriter):
#     list_song_id_songwriter = []
#     query(f'SELECT id_song FROM songwriter_write_song WHERE id_songwriter = \'{id_songwriter}\'')
#     list_song_id_songwriter = cursor.fetchall()

#     list_album_id_songwriter = []
#     for song in list_song_id_songwriter:
#         query(f'SELECT id_album FROM SONG WHERE id_konten = \'{song[0]}\'')
#         list_album_id_songwriter.append(cursor.fetchone())

#     return list_album_id_songwriter