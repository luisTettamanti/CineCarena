from cgitb import reset
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from AppCine.forms import PeliculaForm, ActorPeliculaFormSet
from AppCine.models import Pelicula, Actor, Director, Categoria
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db import transaction
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json

log = logging.getLogger(__name__)


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
    template_name = 'peliculaConForm2.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormModificar(UpdateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'peliculaConForm2.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormBorrar(DeleteView):
    model = Pelicula
    template_name = 'peliculaConFormBorrar.html'
    success_url = reverse_lazy('peliculasListaConForm')


class peliculaConFormDetalle(DetailView):
    model = Pelicula
    template_name = 'peliculaConFormDetalle.html'
    context_object_name = 'pelicula'


class Peliculaslista(ListView):
    model = Pelicula
    template_name = 'peliculaslistaoc.html'
    context_object_name = 'peliculas'


# class PeliculaCreateView(CreateView):
#     model = Pelicula
#     form_class = PeliculaForm
#     template_name = 'peliculaForm.html'
#     success_url = reverse_lazy('peliculaslistaoc')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['actores'] = ActorPeliculaFormSet(self.request.POST)
#         else:
#             data['actores'] = ActorPeliculaFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         actores = context['actores']
#
#         if form.is_valid() and actores.is_valid():
#             self.object = form.save()
#
#             actores.instance = self.object
#             actores.save()
#
#             return redirect(self.success_url)
#         else:
#             return self.form_invalid(form)


# class PeliculaUpdateView(UpdateView):
#     model = Pelicula
#     form_class = PeliculaForm
#     template_name = 'peliculaForm.html'
#     success_url = reverse_lazy('peliculaslistaoc')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['actores'] = ActorPeliculaFormSet(self.request.POST, instance=self.object)
#         else:
#             data['actores'] = ActorPeliculaFormSet(instance=self.object)
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         actores = context['actores']
#
#         try:
#             if form.is_valid() and actores.is_valid():
#                 self.object = form.save()
#
#                 actores.instance = self.object
#                 actores.save()
#
#                 return redirect(self.success_url)
#             else:
#                 return self.form_invalid(form)
#
#         except Exception as e:
#             print(f"Ocurrió un error: {e}")
#             return self.form_invalid(form)


class PeliculaCreateView(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = "peliculaForm.html"   # fallback página completa
    formset_prefix = "actores"

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        actores = ActorPeliculaFormSet(instance=None, prefix=self.formset_prefix)
        ctx = {"form": form, "actores": actores}
        if is_htmx(request):
            return render(request, "_peliculaForm.html", ctx)  # parcial offcanvas
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        actores = ActorPeliculaFormSet(request.POST, instance=None, prefix=self.formset_prefix)
        if form.is_valid() and actores.is_valid():
            with transaction.atomic():
                self.object = form.save()              # ahora tenemos pk
                actores.instance = self.object
                actores.save()
            if is_htmx(request):
                return HttpResponse(status=204)        # el <form> cierra y refresca
            return redirect(self.get_success_url())
        status = 422
        tpl = "_peliculaForm.html" if is_htmx(request) else self.template_name
        return render(request, tpl, {"form": form, "actores": actores}, status=status)


# class PeliculaUpdateView(UpdateView):
#     model = Pelicula
#     form_class = PeliculaForm
#     template_name = 'peliculaForm.html'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if is_htmx(request):
#             return render(request, '_peliculaForm.html', {'form': form})
#         return render(request, self.template_name, {'form': form})
#
#     def form_valid(self, form):
#         self.object = form.save()
#         if is_htmx(self.request):
#             return HttpResponse(status=204)
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         if is_htmx(self.request):
#             return render(self.request, '_peliculaForm.html', {'form': form}, status=422)
#         return render(self.request, self.template_name, {'form': form}, status=422)


def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'


class PeliculaUpdateView(UpdateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = "peliculaForm.html"               # página completa (fallback)
    success_url = reverse_lazy("peliculaslistaoc")
    formset_prefix = "actores"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        actores = ActorPeliculaFormSet(instance=self.object, prefix=self.formset_prefix)
        if is_htmx(request):
            return render(request, "_peliculaForm.html", {"form": form, "actores": actores})
        return render(request, self.template_name, {"form": form, "actores": actores})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        actores = ActorPeliculaFormSet(request.POST, instance=self.object, prefix=self.formset_prefix)
        if form.is_valid() and actores.is_valid():
            with transaction.atomic():
                self.object = form.save()
                actores.instance = self.object
                actores.save()
            if is_htmx(request):
                return HttpResponse(status=204)  # el <form> cerrará y refrescará el tbody
            return redirect(self.get_success_url())
        # inválido
        status = 422
        tpl = "_peliculaForm.html" if is_htmx(request) else self.template_name
        return render(request, tpl, {"form": form, "actores": actores}, status=status)


def PeliculaActorAddForm(request, pk):
    if request.method != "POST" or request.headers.get("HX-Request") != "true":
        return HttpResponseBadRequest("HTMX POST requerido.")

    peli = get_object_or_404(Pelicula, pk=pk)
    prefix = "actores"
    fs = ActorPeliculaFormSet(request.POST, instance=peli, prefix=prefix)

    new_index = fs.total_form_count()
    empty = fs.empty_form
    empty.prefix = f"{prefix}-{new_index}"

    row_html = render_to_string("_actorFormRow.html", {"f": empty})
    mgmt_html = render_to_string("_formsetTotalOOB.html", {
        "prefix": prefix,
        "new_total": new_index + 1
    })
    # (opcional) quitar placeholder "Sin actores"
    remove_empty_html = '<tr id="sinActoresRow" hx-swap-oob="true" style="display:none"></tr>'

    return HttpResponse(row_html + mgmt_html + remove_empty_html)


def PeliculaActorAddFormNew(request):  # CREAR (sin pk)
    if request.method != "POST" or not is_htmx(request):
        return HttpResponseBadRequest("HTMX POST requerido.")
    prefix = "actores"
    fs = ActorPeliculaFormSet(request.POST, instance=None, prefix=prefix)
    new_index = fs.total_form_count()
    empty = fs.empty_form
    empty.prefix = f"{prefix}-{new_index}"
    row_html = render_to_string("_actorFormRow.html", {"f": empty})
    mgmt_html = render_to_string("_formsetTotalOOB.html", {"prefix": prefix, "new_total": new_index + 1})
    return HttpResponse(row_html + mgmt_html)


def PeliculasTbody(request):
    peliculas = Pelicula.objects.all().select_related('idDirector')  # ordená como uses
    return render(request, '_peliculasTbody.html', {'peliculas': peliculas})


class PeliculaDeleteView(DeleteView):
    model = Pelicula
    template_name = 'peliculaConFormBorrar.html'
    success_url = reverse_lazy('peliculaslistaoc')


class PeliculaDetailView(DetailView):
    model = Pelicula
    template_name = 'peliculaDetail.html'
    context_object_name = 'pelicula'


class PeliculaDetailViewOC(DetailView):
    model = Pelicula
    template_name = "peliculaDetail.html"  # página completa

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            return render(self.request, "_peliculaDetail.html", context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)
