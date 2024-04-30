import uuid
from django.db import models

class Genre(models.Model):
    id_konten = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    genre = models.CharField(max_length=50)

    class Meta:
        unique_together = ('id_konten', 'genre')

class Lagu(models.Model):
    id_konten = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    id_artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='songs')
    id_album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs')
    total_play = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='songs')

class Album(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField(default=0)
    id_label = models.ForeignKey('Label', on_delete=models.CASCADE, related_name='albums')
    total_durasi = models.IntegerField(default=0)

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email_akun = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey('PemilikHakCipta', on_delete=models.CASCADE, related_name='artists')

class Songwriter(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email_akun = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey('PemilikHakCipta', on_delete=models.CASCADE, related_name='songwriters')