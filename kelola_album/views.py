import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime
from django.urls import reverse

from utils.session_data import get_session_data

def create_album(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        label = request.POST.get('label')
        id_album = str(uuid.uuid4())
        query(f'insert into album values (\'{id_album}\', \'{judul}\', 0, \'{label}\', 0)')
        connection.commit()
        url = reverse('kelola_album:create_lagu')
        url += f'?album_id={id_album}'
        return redirect(url)
    
    contextt = get_session_data(request)
    list_label = query(f'select id, nama from label')
    context = {'list_label': list_label,
               'context': contextt
               }
    return render(request, 'create_album.html', context)


def create_lagu(request):
    isArtist = request.session.get('is_artist')
    isSongwriter = request.session.get('is_songwriter')
    email = request.session.get('email')
    idArtist = query(f'select id from artis where email_akun = \'{email}\'' )
    idSongwriter = query(f'select id from songwriter where email_akun = \'{email}\'' )
    album_id = request.GET.get('album_id')
    nama_artist = ""
    nama_songwriter = ""
    contextt = get_session_data(request)

    if (isArtist):
        isArtist = 'True'
    if (isSongwriter):
        isSongwriter = 'True'

    if request.method == 'POST':
        judul = request.POST.get('judul')
        id_song = str(uuid.uuid4())
        durasi = request.POST.get('durasi')
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year
        year_now = '{:04d}'.format(current_year)
        songwriters = request.POST.getlist('songwriter[]')
        genres = request.POST.getlist('genre[]')

        id_artist, id_pemilik_hak_cipta_artist = get_artist_details(request, isArtist, idArtist)

        insert_konten(id_song, judul, date_now, year_now, durasi)
        insert_song(id_song, id_artist, album_id)
        insert_songwriter_write_song(id_song, songwriters)
        insert_genres(id_song, genres)
        insert_royalti(id_pemilik_hak_cipta_artist, id_song)
        insert_royalti_label(album_id, id_song)
        update_album(album_id, durasi)


        connection.commit()
        return redirect('kelola_album:list_album_edit')

    records_artist = get_artist_records()
    records_songwriter = get_songwriter_records()
    records_genre = get_genre_records()
    judul_album = get_album_title(album_id)
    nama_artist = get_artist_name(isArtist, idArtist)
    nama_songwriter = get_songwriter_name(isSongwriter, idSongwriter)
    list_label = query(f'select id, nama from label')

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
        'labels': list_label,
        'context': contextt
    }


    return render(request, 'create_lagu.html', context)

def list_album(request):
    email = request.session.get('email')
    label = get_label_by_email(email)
    contextt = get_session_data(request)


    if label:
        id_label = str(label['id'])
        records_album = get_albums_by_label(id_label)
        j = []
        for i in records_album:
            {
                'id': str(i['id']),
                'jumlah_lagu': i['jumlah_lagu'],
                'total_durasi': i['total_durasi']
            }
            print(i)
            j.append(i)
        context = {
            'role': 'label',
            'status': 'success',
            'id': str(label['id']),
            'nama': label['nama'],
            'email': label['email'],
            'kontak': label['kontak'],
            'id_pemilik_hak_cipta': str(label['id_pemilik_hak_cipta']),
            'records_album': j,
            'context': contextt

        }

        # print(records_album)
        # print(context)

        response = render(request, 'list_album.html', context)
        # set_label_cookies(response, label)
        return response

    return render(request, 'list_album.html')

def list_album_edit(request):
    isArtist = request.session.get('is_artist')
    isSongwriter = request.session.get('is_songwriter')
    email =  request.session.get('email')
    records_album_artist = []
    records_album_songwriter = []
    artistHasAlbum = False
    songwriterHasAlbum = False
    contextt = get_session_data(request)


    if isArtist == True:
        isArtist = "True"
        id_artis = query(f'select id from artis where email_akun = \'{email}\'' )
        list_album_id_artist = get_album_ids_by_artist(id_artis)

        if list_album_id_artist:
            artistHasAlbum = True
            records_album_artist = get_album_records_by_ids(list_album_id_artist)

    if isSongwriter == True:
        isSongwriter = "True"
        id_songwriter = query(f'select id from songwriter where email_akun = \'{email}\'' )
        list_album_id_songwriter = get_album_ids_by_songwriter(id_songwriter)

        if list_album_id_songwriter:
            songwriterHasAlbum = True
            records_album_songwriter = get_album_records_by_ids(list_album_id_songwriter)

    context = {
        'status': 'success',
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'artistHasAlbum': artistHasAlbum,
        'songwriterHasAlbum': songwriterHasAlbum,
        'records_album_artist': records_album_artist,
        'records_album_songwriter': records_album_songwriter,
        'context': contextt
    }

    response = render(request, 'list_album_edit.html', context)
    return response

def list_song(request):
    album_id = request.GET.get('album_id')
    records_song = get_song_records_by_album(album_id)
    contextt = get_session_data(request)

    context = {
        'status': 'success',
        'records_song': records_song,
        'context': contextt
    }
    response = render(request, 'list_lagu.html', context)
    return response

def delete_album(request):
    album_id = request.GET.get('album_id') 
    query(f'delete from album where id = \'{album_id}\'')
    connection.commit()
    return redirect('kelola_album:list_album_edit')

def delete_lagu(request):
    id_lagu = request.GET.get('id_lagu')
    print(id_lagu)
    query(f'delete from song where id_konten = \'{id_lagu}\'')
    connection.commit()
    return redirect('kelola_album:list_album_edit')


def get_artist_details(request, isArtist, idArtist):
    if isArtist == "True":
        id_artist = idArtist
        id_pemilik_hak_cipta_artist = request.session.get('id_pemilik_cipta_artist')
    else:
        id_artist = request.POST.get('artist')
        response =  query(f'select id_pemilik_hak_cipta from artis where id = \'{id_artist}\'')
        if response:  # Check if the query returned any results
            id_pemilik_hak_cipta_artist = response[0]  # Get the first result
        else:
            id_pemilik_hak_cipta_artist = None  # No results, set to None or a default value
    return id_artist, id_pemilik_hak_cipta_artist


def insert_konten(id_song, judul, date_now, year_now, durasi):
    query(f'insert into konten values (\'{id_song}\', \'{judul}\', \'{date_now}\', \'{year_now}\', \'{durasi}\')')

def insert_song(id_song, id_artist, album_id):
    res = query(f"insert into song values (\'{id_song}\', \'{id_artist[0]['id']}\', \'{album_id}\', 0, 0)")
    

def insert_songwriter_write_song(id_song, songwriters):
    for songwriter in songwriters:
        idsongwriter = query(f'select id from songwriter where id = \'{songwriter}\'')
        query(f"insert into royalti values (\'{idsongwriter[0]['id']}\', \'{id_song}\', 0)")
        query(f'insert into songwriter_write_song values (\'{songwriter}\', \'{id_song}\')')

def insert_genres(id_song, genres):
    for genre in genres:
        query(f'insert into genre values (\'{id_song}\', \'{genre}\')')

def insert_royalti(id_pemilik_hak_cipta, id_song):
    res = query(f'insert into royalti values (\'{id_pemilik_hak_cipta}\', \'{id_song}\', 0)')

def insert_royalti_label(album_id, id_song):
    id_label = query(f'select id_label from album where id = \'{album_id}\'')
    id_pemilik_hak_cipta_label = query(f'select id_pemilik_hak_cipta from label where id = \'{album_id}\'')
    query(f'insert into royalti values (\'{id_pemilik_hak_cipta_label}\', \'{id_song}\', 0)')

# TODO: Delete kalo udah ada
def update_album(album_id, durasi):
    album_saat_ini = query(f'select jumlah_lagu, total_durasi from album where id = \'{album_id}\'')
    new_total_durasi = int(album_saat_ini[0]['total_durasi']) + int(durasi)
    new_jumlah_lagu = int(album_saat_ini[0]['jumlah_lagu']) + 1
    query(f'UPDATE album SET jumlah_lagu = {new_jumlah_lagu}, total_durasi = {new_total_durasi} WHERE id = \'{album_id}\'')

def get_artist_records():
    records_artist = query(f'SELECT id, email_akun, id_pemilik_hak_cipta FROM ARTIS')
    for i in range(len(records_artist)):
        res = query(f'select nama from akun where email = \'{records_artist[i]["email_akun"]}\'')
        if res:  # Check if the query returned any results
            res = res[0]  # Get the first result
        else:
            res = None  # No results, set to None or a default value
        records_artist[i]["nama"] = res
    return records_artist


def get_songwriter_records():
    records_songwriter = query(f'select id, email_akun, id_pemilik_hak_cipta from songwriter')
    for i in range(len(records_songwriter)):
        res = query(f'select nama from akun where email = \'{records_songwriter[i]["email_akun"]}\'')
        if res:  # Check if the query returned any results
            res = res[0]  # Get the first result
        else:
            res = None  # No results, set to None or a default value
        records_songwriter[i]["nama"] = res
    return records_songwriter


def get_genre_records():
    records_genre = query(f'select distinct genre from genre')
    return records_genre


def get_album_title(album_id):
    judul_album = query(f'select judul from album where id = \'{album_id}\'')
    return judul_album

def get_artist_name(isArtist, idArtist):
    nama_artist = ""
    if isArtist == "True":
        email_artist = query(f"select email_akun from artis where id = \'{idArtist[0]['id']}\'")
        nama_artist = query(f"select nama from akun where email = \'{email_artist[0]['email_akun']}\'")
    return nama_artist

def get_songwriter_name(isSongwriter, idSongwriter):
    nama_songwriter = ""
    if isSongwriter == "True":
        email_songwriter = query(f'select email_akun from songwriter where id = \'{idSongwriter}\'')
        nama_songwriter = query(f'select nama from akun where email = \'{email_songwriter}\'')
    return nama_songwriter

def get_label_by_email(email):
    label = query(f'select * from label where email = \'{email}\'')
    return label[0] if label else None


def get_albums_by_label(id_label):
    records_album = query(f'select * from album where id_label = \'{id_label}\'')
    return records_album


# def set_label_cookies(response, label):
#     print()
#     response.session['role'] = 'label'
#     response.session['email'] = label['email']
#     response.session['id'] = str(label['id'])
#     response.session['id_pemilik_cipta_label'] = str(label['id_pemilik_cipta_label'])

def get_album_ids_by_artist(id_artist):
    list_album_id_artist = query(f"SELECT DISTINCT id_album FROM SONG WHERE id_artist = \'{id_artist[0]['id']}\'")
    return list_album_id_artist


def get_album_records_by_ids(list_album_ids):
    records_album = []
    for id_album in list_album_ids:
        album_record = query(f"SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album['id_album']}\'")
        res = query(f"SELECT nama FROM LABEL WHERE id = \'{album_record[0]['id_label']}\'")
        album_record = album_record + res
        records_album.append(album_record)
    return records_album

def get_album_ids_by_songwriter(id_songwriter):
    list_song_id_songwriter = query(f"SELECT id_song FROM songwriter_write_song WHERE id_songwriter = \'{id_songwriter[0]['id']}\'")
    list_album_id_songwriter = []
    for song in list_song_id_songwriter:
        res = query(f'SELECT id_album FROM SONG WHERE id_konten = \'{song["id_song"]}\'')
        if res[0] not in list_album_id_songwriter:
            list_album_id_songwriter.append(res[0])  # Get the first result
    return list_album_id_songwriter


def get_song_records_by_album(album_id):
    records_song = query(f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    if isinstance(records_song, Exception):  # Check if the query returned an error
        print(f"Error executing query: {records_song}")
        return []
    for i in range(len(records_song)):
        res = query(f"SELECT judul, tanggal_rilis, tahun, durasi from konten where id = \'{records_song[i]['id_konten']}\'")
        records_song[i] = [records_song[i]] + [res[0]]

    return records_song

