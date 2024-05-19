from django.shortcuts import render
from utils.query import query
from utils.session_data import get_session_data
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
def show_download(request):
    context = get_session_data(request)
    print(2)
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader,ds.id_song
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id
                    WHERE DS.email_downloader= '{context['email']}'"""
    hasil = query(query_str)
    return render(request, 'download/index.html', {'konten': hasil,'context':context})

def show_download_by_email(request,email):
    print(1)
    query_str = f"""SELECT AK.nama, K.judul, ds.email_downloader, ds.id_song
                    FROM downloaded_song DS
                    LEFT JOIN song S ON DS.id_song = S.id_konten
                    LEFT JOIN artis A ON S.id_artist = A.id
                    LEFT JOIN akun AK ON A.email_akun = AK.email
                    LEFT JOIN konten K ON DS.id_song = K.id
                    WHERE DS.email_downloader= '{email}'"""
    hasil = query(query_str)
    return render(request, 'download/index.html', {'konten': hasil})

@csrf_exempt
def delete_download(request):
     if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = QueryDict(body_unicode)
        
        
        
       
        song = body_data.get('song')
        email = body_data.get('email')

        query_delete = f"""DELETE FROM DOWNLOADED_SONG
                            WHERE id_song = '{song}'
                            AND email_downloader = '{email}';"""
        query(query_delete)
        return HttpResponse("Delete success", status=200)
     else:
        return HttpResponse("Delete failed", status=400)