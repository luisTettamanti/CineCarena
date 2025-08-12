from cgitb import reset
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from AppCine.forms import PeliculaForm
from AppCine.models import Pelicula, Actor, Director, Categoria
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


# def index(request):
#     mensaje = f"<html><h1>Bienvenidos a Cine Carena</h1> " \
#               f"<p>Ya tenemos algunas películas...!<p></html>"
#     return HttpResponse(mensaje)


def index(request):
    peliculas = Pelicula.objects.filter(ordenNetflix__isnull=False)
    contexto = {'fecha_actual': datetime.now(), 'nombre': 'Luis', 'peliculas': peliculas}
    return render(request, 'index.html', contexto)


def pelicula(request):
    nombre = request.GET.get('nombre', None)
    return render(request, 'pelicula.html', {'nombre': nombre})


def peliculadatos(request):
    nombre = request.GET.get('nombre', None)
    pelicula = get_object_or_404(Pelicula, nombre=nombre)
    return render(request, 'peliculadatos.html', {'pelicula': pelicula})


def peliculaslistanetflix(request):
    peliculas = Pelicula.objects.all().order_by('ordenNetflix')
    return render(request, 'peliculaslistanetflix.html', {'peliculas': peliculas})


def peliculadatosnetflix(request):
    id = request.GET.get('id', None)
    pelicula = get_object_or_404(Pelicula, id=id)
    return render(request, 'peliculadatosnetflix.html', {'pelicula': pelicula})


def actoreslista(request):
    actores = Actor.objects.all().order_by('nombre')
    return render(request, 'actoreslista.html', {'actores': actores})


def actordatos(request, pk):
    actor = get_object_or_404(Actor, id=pk)
    return render(request, 'actordatos.html', {'actor': actor})


def peliculaForm(request, pk=None):
    directores = Director.objects.all()
    categorias = Categoria.objects.all()
    pelicula = None

    if pk:
        pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        anio = request.POST.get('anio')
        duracion = request.POST.get('duracion')
        idDirector = request.POST.get('idDirector')
        imdb = request.POST.get('imdb')
        imdb = imdb if imdb else None
        idCategoria = request.POST.get('idCategoria')
        ordenNetflix = request.POST.get('ordenNetflix')
        ordenNetflix = int(ordenNetflix) if ordenNetflix else None
        caratula = request.POST.get('caratula')
        resenia = request.POST.get('resenia')

        if nombre and anio and duracion:
            if pelicula:
                # actualizar
                pelicula.nombre = nombre
                pelicula.anio = anio
                pelicula.duracion = duracion
                pelicula.idDirector_id = idDirector
                pelicula.imdb = imdb
                pelicula.idCategoria_id = idCategoria
                pelicula.ordenNetflix = ordenNetflix
                pelicula.caratula = caratula
                pelicula.resenia = resenia
                pelicula.save()
            else:
                # crear
                Pelicula.objects.create(
                    nombre=nombre,
                    anio=anio,
                    duracion=duracion,
                    idDirector_id=idDirector,
                    imdb=imdb,
                    idCategoria_id=idCategoria,
                    ordenNetflix=ordenNetflix,
                    caratula=caratula,
                    resenia=resenia
                )
            return redirect('peliculaslista')

    return render(request, 'peliculaform.html', {
        'directores': directores,
        'categorias': categorias,
        'pelicula': pelicula
    })


def peliculaBorrar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        pelicula.delete()
        return redirect('peliculaslista')  # nombre de tu vista de listado

    # Si es GET, mostramos una página de confirmación
    return render(request, 'peliculaconfborrar.html', {'pelicula': pelicula})


def peliculaConsultar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    return render(request, 'peliculadatos.html', {'pelicula': pelicula})


def peliculasLista(request):
    peliculas = Pelicula.objects.all()
    context = {"peliculas": peliculas}
    return render(request, "peliculaslista.html", context)


class peliculasListaConForm(ListView):
    model = Pelicula
    template_name = 'peliculasListaConForm.html'
    context_object_name = 'peliculas'


class peliculaConFormAgregar(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'peliculaConForm.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormModificar(UpdateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'peliculaConForm.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormBorrar(DeleteView):
    model = Pelicula
    template_name = 'peliculaConFormBorrar.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormDetalle(DetailView):
    model = Pelicula
    template_name = 'peliculaConFormDetalle.html'
    context_object_name = 'pelicula'