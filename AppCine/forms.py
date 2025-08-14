from django import forms
from .models import Pelicula

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'anio': forms.NumberInput(attrs={'class':'form-control'}),
            'duracion': forms.NumberInput(attrs={'class':'form-control'}),
            'idDirector': forms.Select(attrs={'class':'form-select'}),
            'imdb': forms.NumberInput(attrs={'class':'form-control'}),
            'idCategoria': forms.Select(attrs={'class':'form-select'}),
            'ordenNetflix': forms.NumberInput(attrs={'class':'form-control'}),
            'caratula': forms.URLInput(attrs={'class': 'form-control'}),
            'resenia': forms.Textarea(attrs={'class': 'form-control'}),
            'actores': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }