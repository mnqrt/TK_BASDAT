from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateAlbumForm, CreateLaguForm
from .models import Album, Lagu

def album_views(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    if request.method == 'GET':
        # Render the CREATE ALBUM form
        create_album_form = CreateAlbumForm()
        albums = Album.objects.all()
        context = {
            'create_album_form': create_album_form,
            'albums': albums
        }
        return render(request, 'album/create_album.html', context)

    elif request.method == 'POST':
        # Handle the CREATE ALBUM form submission
        create_album_form = CreateAlbumForm(request.POST)
        if create_album_form.is_valid():
            judul = create_album_form.cleaned_data['judul']
            label = create_album_form.cleaned_data['label']
            album = Album.objects.create(judul=judul, label=label)
            # Redirect to the CREATE LAGU page for the new album
            return redirect(reverse('create_lagu', args=[album.id]))

def create_lagu(request, album_id):
    album = Album.objects.get(id=album_id)

    if request.method == 'GET':
        # Render the CREATE LAGU form
        create_lagu_form = CreateLaguForm(initial={'album': album})
        context = {
            'album': album,
            'create_lagu_form': create_lagu_form
        }
        return render(request, 'album/create_lagu.html', context)

    elif request.method == 'POST':
        # Handle the CREATE LAGU form submission
        create_lagu_form = CreateLaguForm(request.POST)
        if create_lagu_form.is_valid():
            judul = create_lagu_form.cleaned_data['judul']
            artist = create_lagu_form.cleaned_data['artist']
            songwriter = create_lagu_form.cleaned_data['songwriter']
            genre = create_lagu_form.cleaned_data['genre']
            durasi = create_lagu_form.cleaned_data['durasi']
            lagu = Lagu.objects.create(
                judul=judul, artist=artist, songwriter=songwriter,
                genre=genre, durasi=durasi, album=album
            )
            # Redirect to the DAFTAR LAGU page for the album
            return redirect(reverse('daftar_lagu', args=[album.id]))

def daftar_lagu(request, album_id):
    album = Album.objects.get(id=album_id)
    lagus = Lagu.objects.filter(album=album)
    context = {
        'album': album,
        'lagus': lagus
    }
    return render(request, 'album/daftar_lagu.html', context)