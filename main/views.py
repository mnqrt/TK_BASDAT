import json
import random
import uuid
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, QueryDict, JsonResponse
from utils.query import query
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from utils.session_data import get_session_data

MAP_GENDER = {0:'perempuan',1:'laki-laki'}
MAP_ROLE = {True:'verified',False:'not verified'}
def show_homepage(request):
    context = get_session_data(request)

    if not context['is_label']:
        context['data'] = query(f"SELECT * FROM AKUN WHERE email = '{context['email']}'")
        query_str = f"SELECT * FROM USER_PLAYLIST WHERE email_pembuat='{context['email']}'"
        user_playlists = query(query_str)

        for user_playlist in user_playlists:
            user_playlist['tanggal_dibuat'] = user_playlist['tanggal_dibuat'].strftime('%Y-%m-%d')

        context['playlist'] = user_playlists
        context['playlist_length'] = len(context['playlist'])
    else:
        context['data'] = query(f"SELECT * FROM LABEL WHERE email = '{context['email']}'")


    if context['is_artist']:
        query_str = f"""
                    SELECT K.judul
                    FROM ARTIS A
                    JOIN SONG S ON A.id = S.id_artist
                    JOIN KONTEN K ON K.id = S.id_konten
                    WHERE A.email_akun = '{context['email']}';
                    """
        context['song']=  query(query_str)  
        context['song_length'] = len(context['song'])

    if context['is_songwriter']:
        query_str = f"""
                    SELECT K.judul
                    FROM SONGWRITER S
                    JOIN SONGWRITER_WRITE_SONG SWS ON S.id = SWS.id_songwriter
                    JOIN KONTEN K ON K.id = SWS.id_song
                    WHERE S.email_akun = '{context['email']}'
                    """
        context['song']=  query(query_str)  
        context['song_length'] = len(context['song'])

    if context['is_podcaster']:
        query_str = f"""
                    SELECT K.judul
                    FROM PODCASTER P
                    JOIN PODCAST J ON J.email_podcaster = P.email
                    JOIN KONTEN K ON K.id = J.id_konten
                    WHERE P.email = '{context['email']}';
                    """
        context['podcast']=  query(query_str)  
        context['podcast_length'] = len(context['podcast'])

    if context['is_label']:
        query_str = f"""
                    SELECT A.judul
                    FROM LABEL L 
                    JOIN ALBUM A ON A.id_label = L.id
                    WHERE L.email = '{context['email']}'; 
                    """
        context['album']=  query(query_str)  
        context['album_length'] = len(context['album'])

   

    if context['data'] != []:
        context['data'] = context['data'].pop()
        if not context['is_label']:
            context['data']['gender'] = MAP_GENDER[context['data']['gender']]
            context['data']['is_verified'] = MAP_ROLE[context['data']['is_verified']]
    return render(request, 'main/index.html',{'context':context})


def login_page(request):
    return render(request, 'main/login.html')

# def redirect_page(request):
#     return HttpResponse(
#      'Home Function is redirected to destination_view function')

@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = QueryDict(body_unicode)
        
        email = body_data.get('email')
        password = body_data.get('password')

        query_is_user = f"""SELECT 
                            CASE WHEN EXISTS 
                                (SELECT A.nama
                                FROM AKUN A  
                                WHERE A.email='{email}' and A.password='{password}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        
        query_is_label = f"""SELECT 
                            CASE WHEN EXISTS 
                                (SELECT L.nama
                                FROM LABEL L  
                                WHERE L.email='{email}' and L.password='{password}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        
        query_is_premium = f"""SELECT  
                            CASE WHEN EXISTS 
                                (SELECT P.email
                                FROM PREMIUM P  
                                WHERE P.email='{email}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        
        query_is_songwriter = f"""SELECT  
                            CASE WHEN EXISTS 
                                (SELECT D.email_akun
                                FROM SONGWRITER D  
                                WHERE D.email_akun='{email}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        query_is_artist = f"""SELECT  
                            CASE WHEN EXISTS 
                                (SELECT D.email_akun
                                FROM artis D  
                                WHERE D.email_akun='{email}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        query_is_podcaster = f"""SELECT  
                            CASE WHEN EXISTS 
                                (SELECT D.email
                                FROM podcaster D  
                                WHERE D.email='{email}')
                            THEN 1 
                            ELSE 0 
                            END 
                            """
        
        if query(query_is_label).pop().get('case')== 1:
            request.session["is_label"] = True
        else:
            if query(query_is_user).pop().get('case')== 1:
                if query(query_is_premium).pop().get('case')==1:
                    request.session["is_premium"] = True
                
                if query(query_is_artist).pop().get('case')==1:
                    request.session["is_artist"] = True
                
                if query(query_is_songwriter).pop().get('case')==1:
                    request.session["is_songwriter"] = True
                
                if query(query_is_podcaster).pop().get('case')==1:
                    request.session["is_podcaster"] = True
            else:

                messages.error(request, "Email atau password salah!")
                return HttpResponse("Authentication failed", status=400)
            
        request.session["is_active"] = True
        request.session["email"] = email
        return HttpResponse("OK", status=200)
    
    return HttpResponse("Authentication failed", status=400)      
  
# @login_required
def logout(request):
    session_keys = list(request.session.keys())
    for sesskey in session_keys:
        del request.session[sesskey]
    # auth.logout(request)
    return redirect('main:show_homepage')

def search(request):
    if request.method == 'GET':
        context = get_session_data(request)
        keyword = request.GET.get('query')
        query_result = []

        query_song = f"""SELECT 'SONG' AS tipe, k.judul, ak.nama
                        FROM konten k
                        JOIN song s on k.id = s.id_konten
                        JOIN artis a on s.id_artist = a.id
                        JOIN akun ak on ak.email = a.email_akun
                        WHERE k.judul ~* '(?i){keyword}'
                        """
        query_podcast =f"""SELECT 'PODCAST' AS tipe, k.judul, ak.nama
                        FROM konten k
                        LEFT JOIN podcast p on k.id = p.id_konten
                        LEFT JOIN akun ak on ak.email = p.email_podcaster
                        WHERE k.judul ~* '(?i){keyword}'
                        """
        query_playlist = f"""SELECT 'USER PLAYLIST' AS tipe, up.judul, ak.nama
                            FROM user_playlist up
                            JOIN akun ak on ak.email = up.email_pembuat
                            WHERE up.judul ~* '(?i){keyword}'
                        """
        
        query_result.extend(query(query_song))
        query_result.extend(query(query_podcast))
        query_result.extend(query(query_playlist))
        print(query_result)
        return render(request, 'main/search.html',{'context':context,'konten':query_result,'keyword':keyword})
    
    return HttpResponse("search failed", status=400)

def register_page(request):
    return render(request, 'main/register.html')

def register_label_page(request):
    return render(request, 'main/register_label.html')

def register_pengguna_page(request):
    return render(request, 'main/register_pengguna.html')

def register_label(request):
    pass

@csrf_exempt
def register_pengguna(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    nama = data.get('name')
    gender = 0 if data.get('gender') == "female" else 1
    tempat_lahir = data.get('birthplace')
    tanggal_lahir = data.get('birthdate')
    kota_asal = data.get('city')
    role = data.get('role') 
    is_verified = "TRUE" if role is not None else "FALSE"
    print(data)

    query_str = f"""INSERT INTO AKUN (nama, email, password, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES 
                    ('{nama}', '{email}', '{password}', {gender}, '{tempat_lahir}', '{tanggal_lahir}', {is_verified}, '{kota_asal}')"""
    res = query(query_str)
    if "RAISE" in str(res):
        return JsonResponse({"gagal": "gagal"})

    if role is not None:
        if "Podcaster" in role:
            query(f"INSERT INTO PODCASTER (email) VALUES ('{email}')")
        if "Artist" in role:
            random_uuid = str(uuid.uuid4())
            query(f"INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES ('{random_uuid}', {random.randint(1, 1000)})")
            query(f"INSERT INTO ARTIS (id, email_akun, id_pemilik_hak_cipta) VALUES ('{str(uuid.uuid4())}', '{email}', '{random_uuid}')")
        if "Songwriter" in role:
            random_uuid = str(uuid.uuid4())
            query(f"INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES ('{random_uuid}', {random.randint(1, 1000)})")
            query(f"INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta) VALUES ('{str(uuid.uuid4())}', '{email}', '{random_uuid}')")
    return JsonResponse({"gagal": "tidak gagal"})

@csrf_exempt
def register_label(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    nama = data.get('nama')
    kontak = data.get('kontak')

    random_uuid = str(uuid.uuid4())
    query(f"INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti) VALUES ('{random_uuid}', {random.randint(1, 1000)})")
    res = query(f"""INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES ('{str(uuid.uuid4())}', '{nama}', '{email}', '{password}', '{kontak}', '{random_uuid}')""")
    if "RAISE" in str(res):
        return JsonResponse({"gagal": "gagal"})
    return JsonResponse({"gagal": "tidak gagal"})
