from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from utils.query import query

def chart_list(request):
    with connection.cursor() as cursor:
        query("SELECT id, type FROM chart")
        charts = cursor.fetchall()

    context = {
        'charts': [{'id': chart[0], 'type': chart[1]} for chart in charts]
    }
    return render(request, 'chart_list.html', context)

def chart_detail(request, chart_id):
    with connection.cursor() as cursor:
        query("""
            SELECT type FROM chart WHERE id = %s
        """, [chart_id])
        chart = cursor.fetchone()
        
        query("""
            SELECT title, artist, release_date, total_plays 
            FROM song 
            WHERE chart_id = %s 
            ORDER BY total_plays DESC 
            LIMIT 20
        """, [chart_id])
        songs = cursor.fetchall()

    context = {
        'chart_type': chart[0],
        'songs': [{'title': song[0], 'artist': song[1], 'release_date': song[2], 'total_plays': song[3]} for song in songs]
    }
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