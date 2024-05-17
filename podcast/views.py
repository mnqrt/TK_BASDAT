from django.shortcuts import render
from django.http import JsonResponse
from utils.query import query


def show_podcast(request, podcast_id):
    return render(request, 'podcast_detail.html', {'podcast_id': podcast_id})

def get_podcast_detail_data(request, podcast_id):
    # Query to get the podcast details
    podcast_query = f"""
    SELECT K.judul, K.tanggal_rilis, K.tahun, K.durasi, AK.nama AS podcaster
    FROM podcast P
    JOIN konten K ON P.id_konten = K.id
    JOIN akun AK ON P.email_podcaster = AK.email
    WHERE P.id_konten = '{podcast_id}'
    """
    
    podcast = query(podcast_query)[0]
    
    # Query to get the genres
    genre_query = f"""
    SELECT genre
    FROM genre
    WHERE id_konten = '{podcast_id}'
    """
    
    genres = [row['genre'] for row in query(genre_query)]
    
    # Query to get the episodes
    episode_query = f"""
    SELECT judul, deskripsi, durasi, tanggal_rilis
    FROM episode
    WHERE id_konten_podcast = '{podcast_id}'
    """
    
    episodes = query(episode_query)
    
    # Convert duration to hours and minutes
    def convert_to_hours_minutes(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return hours, minutes
    
    podcast_duration_hours, podcast_duration_minutes = convert_to_hours_minutes(podcast['durasi'])
    for episode in episodes:
        episode['durasi_hours'], episode['durasi_minutes'] = convert_to_hours_minutes(episode['durasi'])
    
    response_data = {
        'podcast': podcast,
        'genres': genres,
        'episodes': episodes,
        'podcast_duration_hours': podcast_duration_hours,
        'podcast_duration_minutes': podcast_duration_minutes,
    }
    
    return JsonResponse(response_data)

def podcast_detail(request, podcast_id):
    cursor = connection.cursor()
    
    # Get podcast details
    cursor.execute("""
        SELECT K.judul AS "Judul",
            array_agg(G.genre) AS "Genre",
            AKUN.nama AS "Podcaster",
            COALESCE(EP.total_durasi, 0) AS "Total Durasi",
            K.tanggal_rilis AS "Tanggal Rilis",
            K.tahun AS "Tahun"
        FROM KONTEN K
        LEFT JOIN PODCAST P ON K.id = P.id_konten
        LEFT JOIN GENRE G ON K.id = G.id_konten
        LEFT JOIN AKUN ON P.email_podcaster = AKUN.email
        LEFT JOIN (
            SELECT id_konten_podcast, SUM(durasi) AS total_durasi
            FROM EPISODE
            GROUP BY id_konten_podcast
        ) AS EP ON P.id_konten = EP.id_konten_podcast
        WHERE K.id = %s
        GROUP BY K.judul, AKUN.nama, K.tanggal_rilis, K.tahun, EP.total_durasi;
    """, [podcast_id])
    podcast_detail = cursor.fetchone()

    # Get episodes for the specified podcast ID
    cursor.execute("""
        SELECT E.id_episode,
                E.judul AS "Judul Episode",
                E.deskripsi AS "Deskripsi",
                E.durasi AS "Durasi",
                E.tanggal_rilis AS "Tanggal"
        FROM EPISODE E
        JOIN PODCAST P ON E.id_konten_podcast = P.id_konten
        JOIN KONTEN K ON P.id_konten = K.id
        WHERE K.id = %s;
    """, [podcast_id])
    episodes = cursor.fetchall()
    
    episode_data = []
    for episode in episodes:
        episode_id = episode[0]
        judul_episode = episode[1]
        deskripsi = episode[2]
        durasi = episode[3]
        tanggal_rilis = episode[4]
        episode_data.append({
            'id': episode_id,
            'judul': judul_episode,
            'deskripsi': deskripsi,
            'durasi_hours': durasi // 60,
            'durasi_minutes': durasi % 60,
            'tanggal_rilis': tanggal_rilis
        })
    
    total_duration_minutes = podcast_detail[3]
    total_hours = total_duration_minutes // 60
    total_minutes = total_duration_minutes % 60

    context = {
        'podcast_detail': {
            'judul': podcast_detail[0],
            'genre': podcast_detail[1],
            'podcaster': podcast_detail[2],
            'total_durasi_hours': total_hours,
            'total_durasi_minutes': total_minutes,
            'tanggal_rilis': podcast_detail[4],
            'tahun': podcast_detail[5],
        },
        'episodes': episode_data
    }

    return render(request, 'podcast_detail.html', context)
