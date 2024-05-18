from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, QueryDict
from utils.query import query
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from utils.session_data import get_session_data

def show_homepage(request):
    context = get_session_data(request)
    print(context)
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
        
        query_id_label = f"""
                        SELECT L.id_pemilik_hak_cipta
                        FROM label L, pemilik_hak_cipta P
                        WHERE L.id_pemilik_hak_cipta = P.id AND L.email='{email}' 
                        """

        query_id_songwriter = f"""
                        SELECT S.id_pemilik_hak_cipta
                        FROM songwriter S, akun AK, pemilik_hak_cipta P
                        WHERE S.id_pemilik_hak_cipta = P.id AND AK.email='{email}' AND AK.email=S.email_akun
                        """

        
        query_id_artis = f"""
                        SELECT A.id_pemilik_hak_cipta
                        FROM artis A, akun AK, pemilik_hak_cipta P
                        WHERE A.id_pemilik_hak_cipta = P.id AND AK.email='{email}' AND AK.email=A.email_akun
                        """


        if query(query_is_label).pop().get('case')== 1:
            request.session["is_label"] = True
            result_label = query(query_id_label)
            request.session["id_pemilik_cipta_label"] = result_label[0]['id_pemilik_hak_cipta']

        else:
       
            if query(query_is_user).pop().get('case')== 1:

                if query(query_is_premium).pop().get('case')==1:
                    request.session["is_premium"] = True
                
                if query(query_is_artist).pop().get('case')==1:
                    request.session["is_artist"] = True
                    result_artis = query(query_id_artis)
                    request.session["id_pemilik_cipta_artist"] = result_artis[0]['id_pemilik_hak_cipta']

                if query(query_is_songwriter).pop().get('case')==1:
                    request.session["is_songwriter"] = True
                    result_songwriter = query(query_id_songwriter)
                    request.session["id_pemilik_cipta_songwriter"] = result_songwriter[0]['id_pemilik_hak_cipta']
                
                if query(query_is_podcaster).pop().get('case')==1:
                    request.session["is_podcaster"] = True
            else:

                messages.error(request, "Email atau password salah!")
                return HttpResponse("Authentication failed", status=400)
            
        request.session["is_active"] = True
        request.session["email"] = email
        return HttpResponse("OK", status=200)
            
  
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

