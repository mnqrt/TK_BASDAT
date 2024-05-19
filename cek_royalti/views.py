import uuid
from django.shortcuts import render
from utils.query import *
from utils.session_data import get_session_data

def get_royalty_records(id_pemilik_hak_cipta):
    response = query(
        f'SELECT r.id_song, r.jumlah, s.id_album, s.total_play, s.total_download, a.judul AS judul_album, k.judul AS judul_lagu '
        f'FROM royalti r '
        f'JOIN song s ON r.id_song = s.id_konten '
        f'JOIN album a ON s.id_album = a.id '
        f'JOIN konten k ON s.id_konten = k.id '
        f'WHERE r.id_pemilik_hak_cipta = \'{id_pemilik_hak_cipta}\''
    )
    # print(cursor.fetchall())
    print("hello")
    print(response)
    return response

def cek_royalti(request):
    role = request.session.get('is_label')
    is_artist = request.session.get('is_artist') == True
    is_songwriter = request.session.get('is_songwriter') == True
    contextt = get_session_data(request)

    records_royalti_label = []
    records_royalti_artist = []
    records_royalti_songwriter = []

    if role == True:
        role = 'label'
        id_pemilik_cipta_label = request.session.get('id_pemilik_cipta_label')
        records_royalti_label = get_royalty_records(id_pemilik_cipta_label)
    else:
        role = 'pengguna'
        if is_artist:
            id_pemilik_cipta_artist = request.session.get('id_pemilik_cipta_artist')
            records_royalti_artist = get_royalty_records(id_pemilik_cipta_artist)
            is_artist = 'True'
        if is_songwriter:
            id_pemilik_cipta_songwriter = request.session.get('id_pemilik_cipta_songwriter')
            records_royalti_songwriter = get_royalty_records(id_pemilik_cipta_songwriter)
            is_songwriter = 'True'

    context = {
        'status': 'success',
        'role': role,
        'isArtist': is_artist,
        'isSongwriter': is_songwriter,
        'records_royalti_label': records_royalti_label,
        'records_royalti_artist': records_royalti_artist,
        'records_royalti_songwriter': records_royalti_songwriter,
        'context': contextt
    }
    response = render(request, 'cek_royalti.html', context)
    
    return response
