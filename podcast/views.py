from django.shortcuts import render
from utils.query import *
import uuid

def play_podcast(request, podcast_id):
    connection, cursor = query()

    podcast_id_str = str(podcast_id)  # Convert UUID to string

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
    """, [podcast_id_str])
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
    """, [podcast_id_str])
    episodes = cursor.fetchall()

    episode_data = []
    for episode in episodes:
        episode_id = episode[0]
        judul_episode = episode[1]
        deskripsi = episode[2]
        durasi = episode[3]
        tanggal_rilis = episode[4]

        episode_duration_hours = durasi // 60
        episode_duration_minutes = durasi % 60

        episode_data.append({
            'id': episode_id,
            'judul': judul_episode,
            'deskripsi': deskripsi,
            'durasi': durasi,
            'durasi_hours': episode_duration_hours,
            'durasi_minutes': episode_duration_minutes,
            'tanggal_rilis': tanggal_rilis
        })

    podcast_total_duration_minutes = podcast_detail[3]
    podcast_total_hours = podcast_total_duration_minutes // 60
    podcast_total_minutes = podcast_total_duration_minutes % 60

    context = {
        'podcast_detail': {
            'judul': podcast_detail[0],
            'genre': podcast_detail[1],
            'podcaster': podcast_detail[2],
            'total_durasi_hours': podcast_total_hours,
            'total_durasi_minutes': podcast_total_minutes,
            'tanggal_rilis': podcast_detail[4],
            'tahun': podcast_detail[5],
        },
        'episodes': episode_data
    }

    # close connection
    cursor.close()
    connection.close()

    return render(request, 'podcast_detail.html', context)
