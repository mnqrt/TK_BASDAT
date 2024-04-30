from django.shortcuts import render
from utils.query import query
from utils.session_data import get_session_data
def show_download(request):
    context = get_session_data(request)
    print(context)
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id
                    WHERE DS.email_downloader= '{context['email']}'"""
    hasil = query(query_str)
    return render(request, 'download/index.html', {'konten': hasil,'context':context})

def show_download_by_email(request,email):
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id
                    WHERE DS.email_downloader= '{email}'"""
    hasil = query(query_str)
    return render(request, 'download/index.html', {'konten': hasil})
