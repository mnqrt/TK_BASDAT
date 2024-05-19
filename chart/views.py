from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from utils.query import query
def chart_list(request):

    q = query("SELECT id_playlist, tipe FROM CHART")
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT id_playlist, tipe FROM chart")
    #     charts = cursor.fetchall()

    # context = {
    #     'charts': [{'id': chart[0], 'type': chart[1]} for chart in charts]
    # }
    context = {
        'charts': q
    }
    print(q)
    return render(request, 'chart_list.html',context)

def chart_detail(request, chart_id):
    query_type = query(f"SELECT tipe FROM CHART WHERE id_playlist = '{chart_id}'")
    # with connection.cursor() as cursor:
    #     cursor.execute("""
            # SELECT type FROM chart WHERE id = %s
        # """, [chart_id])
        # chart = cursor.fetchone()
        
    #     cursor.execute("""
    #         SELECT title, artist, release_date, total_plays 
    #         FROM song 
    #         WHERE chart_id = %s 
    #         ORDER BY total_plays DESC 
    #         LIMIT 20
    #     """, [chart_id])
    #     songs = cursor.fetchall()
    query_song = query(f"""
                        SELECT K.id,K.judul, AK.nama, K.tanggal_rilis, S.total_play 
                        FROM PLAYLIST_SONG PS
                        JOIN SONG S ON PS.id_song = S.id_konten
                        JOIN ARTIS A ON A.id = S.id_artist
                        JOIN AKUN AK ON AK.email = A.email_akun
                        JOIN KONTEN K ON PS.id_song = K.id
                        WHERE PS.id_playlist = '{chart_id}' 
                        ORDER BY S.total_play DESC 
                        LIMIT 20
                        """)
    context = {
        'chart_type':query_type.pop()['tipe'],
        'songs': query_song
    }

    # print(query_type)
    # print(query_song)
    return render(request, 'chart_detail.html', context)

def get_chart_detail_data(request, chart_id):
    with connection.cursor() as cursor:
        query("""
            SELECT title, artist, release_date, total_plays 
            FROM song 
            WHERE chart_id = %s 
            ORDER BY total_plays DESC 
            LIMIT 20
        """, [chart_id])
        songs = cursor.fetchall()

    data = {
        'songs': [{'title': song[0], 'artist': song[1], 'release_date': song[2], 'total_plays': song[3]} for song in songs]
    }
    return JsonResponse(data)