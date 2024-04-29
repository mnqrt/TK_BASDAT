from django.shortcuts import render
from utils.query import query

def show_download(request):
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id"""
    hasil = query(query_str)
    print(hasil)
    return render(request, 'download/index.html', {'konten': hasil})

def show_download_by_email(request,email):
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id
                    WHERE DS.email_downloader= '{email}'"""
    hasil = query(query_str)
    print(hasil)
    return render(request, 'download/index.html', {'konten': hasil})
