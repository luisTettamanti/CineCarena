from django import forms
from .models import Pelicula, ActorPelicula, Categoria, Director, Actor
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


class ActorPeliculaForm(forms.ModelForm):
    idActor = forms.ModelChoiceField(
        queryset=Actor.objects.all().order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ActorPelicula
        fields = ['id', 'idActor']


ActorPeliculaFormSet = inlineformset_factory(
    Pelicula,
    ActorPelicula,
    form=ActorPeliculaForm,
    extra=3,
    can_delete=True
)


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'fechaNac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'origen': forms.TextInput(attrs={'class':'form-control'}),
        }