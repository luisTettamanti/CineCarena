from django import forms
from .models import Pelicula, ActorPelicula
from django.forms import inlineformset_factory

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        exclude = ('actores',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'anio': forms.NumberInput(attrs={'class':'form-control'}),
            'duracion': forms.NumberInput(attrs={'class':'form-control'}),
            'idDirector': forms.Select(attrs={'class':'form-select'}),
            'imdb': forms.NumberInput(attrs={'class':'form-control'}),
            'idCategoria': forms.Select(attrs={'class':'form-select'}),
            'ordenNetflix': forms.NumberInput(attrs={'class':'form-control'}),
            'caratula': forms.URLInput(attrs={'class': 'form-control'}),
            'resenia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


ActorPeliculaFormSet = inlineformset_factory(Pelicula, ActorPelicula,
    fields=['id', 'idActor'],
    widgets={
        'id': forms.TextInput(attrs={'class': 'form-control'}),
        'idActor': forms.Select(attrs={'class': 'form-select'}),
    },
    extra=0,           # cantidad de formularios en blanco
    can_delete=True    # permitir quitar actores de la película
)