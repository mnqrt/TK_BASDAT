from django.shortcuts import render, redirect
from django.db import connection

def execute_query(query, params=None):
    with connection.cursor() as cursor:
        query(query, params)
        return cursor.fetchall()

def create_podcast(request):
    if request.method == 'POST':
        email_podcaster = request.POST['email_podcaster']
        judul = request.POST['judul']
        tanggal_rilis = request.POST['tanggal_rilis']
        tahun = request.POST['tahun']
        durasi = request.POST['durasi']
        
        query = """
            INSERT INTO podcast (id_konten, email_podcaster, judul, tanggal_rilis, tahun, durasi)
            VALUES (UUID(), %s, %s, %s, %s, %s)
        """
        params = (email_podcaster, judul, tanggal_rilis, tahun, durasi)
        execute_query(query, params)
        return redirect('list_podcast')
    return render(request, 'create_podcast.html')

def list_podcast(request):
    query = "SELECT id_konten, judul, durasi FROM podcast"
    podcasts = execute_query(query)
    return render(request, 'list_podcast.html', {'podcasts': podcasts})

def create_episode(request, podcast_id):
    if request.method == 'POST':
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        durasi = request.POST['durasi']
        tanggal_rilis = request.POST['tanggal_rilis']
        
        query = """
            INSERT INTO episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
            VALUES (UUID(), %s, %s, %s, %s, %s)
        """
        params = (podcast_id, judul, deskripsi, durasi, tanggal_rilis)
        execute_query(query, params)
        return redirect('list_episodes', podcast_id=podcast_id)
    return render(request, 'create_episode.html', {'podcast_id': podcast_id})

def delete_podcast(request, podcast_id):
    query = "DELETE FROM podcast WHERE id_konten = %s"
    execute_query(query, [podcast_id])
    return redirect('list_podcast')

def list_episodes(request, podcast_id):
    query = "SELECT id_episode, judul, deskripsi, durasi, tanggal_rilis FROM episode WHERE id_konten_podcast = %s"
    episodes = execute_query(query, [podcast_id])
    return render(request, 'list_episodes.html', {'episodes': episodes, 'podcast_id': podcast_id})

def delete_episode(request, episode_id):
    query = "DELETE FROM episode WHERE id_episode = %s"
    execute_query(query, [episode_id])
    return redirect('list_podcast')
