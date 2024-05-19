from django.shortcuts import render
from utils.query import *
import uuid

def play_podcast(request, id_podcast):

    id_podcast_str = str(id_podcast)  # Convert UUID to string

    podcast_detail = query(f"""
        SELECT K.judul AS Judul,
            array_agg(G.genre) AS Genre,
            AKUN.nama AS Podcaster,
            COALESCE(EP.total_durasi, 0) AS total_Durasi,
            K.tanggal_rilis AS Tanggal_Rilis,
            K.tahun AS Tahun
        FROM KONTEN K
        LEFT JOIN PODCAST P ON K.id = P.id_konten
        LEFT JOIN GENRE G ON K.id = G.id_konten
        LEFT JOIN AKUN ON P.email_podcaster = AKUN.email
        LEFT JOIN (
            SELECT id_konten_podcast, SUM(durasi) AS total_durasi
            FROM EPISODE
            GROUP BY id_konten_podcast
        ) AS EP ON P.id_konten = EP.id_konten_podcast
        WHERE K.id = '{id_podcast_str}'
        GROUP BY K.judul, AKUN.nama, K.tanggal_rilis, K.tahun, EP.total_durasi
    """)

    # Get episodes for the specified podcast ID
    episodes = query(f"""
        SELECT E.id_episode,
                E.judul AS Judul_Episode,
                E.deskripsi AS Deskripsi,
                E.durasi AS Durasi,
                E.tanggal_rilis AS Tanggal
        FROM EPISODE E
        JOIN PODCAST P ON E.id_konten_podcast = P.id_konten
        JOIN KONTEN K ON P.id_konten = K.id
        WHERE K.id = '{id_podcast_str}'
    """)
    print("::",podcast_detail[0])

    episode_data = []
    for episode in episodes:
        episode_id = episode['id_episode']
        judul_episode = episode['judul_episode']
        deskripsi = episode['deskripsi']
        durasi = episode['durasi']
        tanggal_rilis = episode['tanggal']

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

    podcast_total_duration_minutes = podcast_detail[0]['total_durasi']
    podcast_total_hours = podcast_total_duration_minutes // 60
    podcast_total_minutes = podcast_total_duration_minutes % 60

    print("::::",podcast_detail)
    context = {
        'podcast_detail': {
            'judul': podcast_detail[0]['judul'],
            'genre': podcast_detail[0]['genre'],
            'podcaster': podcast_detail[0]['podcaster'],
            'total_durasi_hours': podcast_total_hours,
            'total_durasi_minutes': podcast_total_minutes,
            'tanggal_rilis': podcast_detail[0]['tanggal_rilis'],
            'tahun': podcast_detail[0]['tahun'],
        },
        'episodes': episode_data
    }

    # close connection

    return render(request, 'podcast_detail.html', context)
