from django import forms
from .models import Album, Genre, Lagu

class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['judul', 'label']

class CreateLaguForm(forms.ModelForm):
    class Meta:
        model = Lagu
        fields = ['judul', 'artist', 'songwriter', 'genre', 'durasi', 'album']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].required = False
        self.fields['songwriter'].required = False
        self.fields['genre'].widget = forms.CheckboxSelectMultiple()
        self.fields['genre'].queryset = Genre.objects.all()