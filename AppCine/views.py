from cgitb import reset
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.timezone import now

from AppCine.forms import PeliculaForm, ActorPeliculaFormSet, CategoriaForm, DirectorForm, ActorForm, PeliculaForm2
from AppCine.models import Pelicula, Actor, Director, Categoria
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db import transaction
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q

from django_tables2.views import SingleTableView
from .tables import PeliculaTable, PeliculaTable2

from django.contrib.auth.views import LoginView, redirect_to_login
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from urllib.parse import urlencode

log = logging.getLogger(__name__)

# def index(request):
#     mensaje = f"<html><h1>Bienvenidos a Cine Carena</h1> " \
#               f"<p>Ya tenemos algunas películas...!<p></html>"
#     return HttpResponse(mensaje)


def index(request):
    peliculas = Pelicula.objects.filter(ordenNetflix__isnull=False)
    contexto = {'fecha_actual': datetime.now(), 'nombre': 'Luis', 'peliculas': peliculas}
    return render(request, 'index.html', contexto)


def mensaje(request):
    return render(request, "_mensaje.html", {'hora': now().strftime("%H:%M:%S")})


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
    ordering = 'nombre'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context


def is_htmx(request):
    return request.headers.get("HX-Request") == "true"


class PeliculaslistaHTMX(ListView):
    model = Pelicula
    template_name = 'peliculaslistaHTMX.html'
    context_object_name = 'peliculas'

    def get_queryset(self):
        qs = (super().get_queryset()
              .select_related('idDirector', 'idCategoria'))
        q = (self.request.GET.get('q') or '').strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(idDirector__nombre__icontains=q) |
                Q(idCategoria__nombre__icontains=q)
            )
        return qs

    def get_template_names(self):
        # 👇 Si es HTMX devolvemos SOLO las filas (sin encabezado ni layout)
        if is_htmx(self.request):
            return ['_peliculasRows.html']
        return [self.template_name]

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


# class PeliculaDeleteView(DeleteView):
#     model = Pelicula
#     template_name = 'peliculaConFormBorrar.html'
#     success_url = reverse_lazy('peliculaslistaoc')


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


class PeliculaDeleteView(DeleteView):
    model = Pelicula
    template_name = "peliculaConFormBorrar.html"  # fallback de página completa

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        ctx = {"object": self.object}
        if is_htmx(request):
            return render(request, "_peliculaconfborraroc.html", ctx)  # 👈 parcial offcanvas
        return render(request, self.template_name, ctx)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except IntegrityError:
            # Por ejemplo, on_delete=PROTECT en relaciones
            ctx = {"object": self.object, "error": "No se puede borrar por referencias relacionadas."}
            if is_htmx(request):
                return render(request, "_peliculaconfborraroc.html", ctx, status=409)
            return render(request, self.template_name, ctx, status=409)

        if is_htmx(request):
            # 204: sin contenido; el form en el offcanvas cerrará y pedirá refresco del listado
            return HttpResponse(status=204)
        return redirect("peliculaslistaoc")


class PeliculasLista2(ListView):
    model = Pelicula
    template_name = 'peliculaslistaoc2.html'
    context_object_name = 'peliculas'
    ordering = 'nombre'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context


class PeliculasLista3(ListView):
    model = Pelicula
    template_name = 'peliculaslistaoc3.html'
    context_object_name = 'peliculas'
    # ordering = 'nombre'
    # paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get("sort", "nombre")  # campo por defecto
        direction = self.request.GET.get("dir", "asc")
        if direction == "desc":
            sort = f"-{sort}"
        return qs.order_by(sort)


class PeliculasLista4(SingleTableView):
    model = Pelicula
    table_class = PeliculaTable
    template_name = "peliculaslistaoc4.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("idDirector", "idCategoria")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(nombre__icontains=q))
        return qs


class peliculaFormModificar2(UpdateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'peliculaForm2.html'
    success_url = reverse_lazy('peliculaslistaoc2')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['actores'] = ActorPeliculaFormSet(self.request.POST, instance=self.object)
        else:
            data['actores'] = ActorPeliculaFormSet(instance=self.object)
        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # --- Categoría nueva ---
        cat_pk = self.request.GET.get("categoria_nueva")
        if cat_pk and "idCategoria" in form.fields:
            form.initial["idCategoria"] = cat_pk
            form.fields["idCategoria"].initial = cat_pk
            # asegurar selección con instancia (ModelForm)
            try:
                form.instance.idCategoria_id = int(cat_pk)
            except (ValueError, TypeError):
                pass

        # --- Director nuevo ---
        dir_pk = self.request.GET.get("director_nuevo")
        # ajustá el nombre del campo si en tu form es distinto (p.ej. "director")
        if dir_pk and "idDirector" in form.fields:
            form.initial["idDirector"] = dir_pk
            form.fields["idDirector"].initial = dir_pk
            try:
                form.instance.idDirector_id = int(dir_pk)
            except (ValueError, TypeError):
                pass

        # --- Actor nuevo ---
        dir_pk = self.request.GET.get("actor_nuevo")
        # ajustá el nombre del campo si en tu form es distinto (p.ej. "director")
        if dir_pk and "idActor" in form.fields:
            form.initial["idActor"] = dir_pk
            form.fields["idActor"].initial = dir_pk
            try:
                form.instance.idDirector_id = int(dir_pk)
            except (ValueError, TypeError):
                pass

        return form

    @transaction.atomic
    def form_valid(self, form):
        # 1) Guardar la película
        self.object = form.save()

        # 2) Reconstruir el formset con la instance YA creada y los datos del POST
        formset = ActorPeliculaFormSet(self.request.POST, instance=self.object)

        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            # si el formset falla, devolvés el template con errores
            return render(self.request, self.template_name, {
                'form': form,
                'actores': formset,
                'object': self.object,
            })


class peliculaFormCrear2(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'peliculaForm2.html'
    success_url = reverse_lazy('peliculaslistaoc2')

    # Preselecciones por querystring (igual que en Modificar)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # --- Categoría nueva ---
        cat_pk = self.request.GET.get("categoria_nueva")
        if cat_pk and "idCategoria" in form.fields:
            form.initial["idCategoria"] = cat_pk
            form.fields["idCategoria"].initial = cat_pk
            try:
                # en CreateView todavía no hay instance persistida; igual podés setearla
                form.instance.idCategoria_id = int(cat_pk)
            except (ValueError, TypeError):
                pass

        # --- Director nuevo ---
        dir_pk = self.request.GET.get("director_nuevo")
        if dir_pk and "idDirector" in form.fields:
            form.initial["idDirector"] = dir_pk
            form.fields["idDirector"].initial = dir_pk
            try:
                form.instance.idDirector_id = int(dir_pk)
            except (ValueError, TypeError):
                pass

        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            # en POST, todavía no guardamos la película; el formset se liga a self.object (None),
            # y luego en form_valid lo re-instanciamos con instance ya creada para validar/guardar
            ctx['actores'] = ActorPeliculaFormSet(self.request.POST, instance=self.object)
        else:
            # GET: podés opcionalmente “sembrar” el primer renglón con actor_nuevo
            actor_pk = self.request.GET.get("actor_nuevo")
            if actor_pk:
                # Esto funciona si tu formset tiene field 'idActor' y al menos extra>=1
                try:
                    initial = [{'idActor': int(actor_pk)}]
                except (ValueError, TypeError):
                    initial = None
                ctx['actores'] = ActorPeliculaFormSet(instance=self.object, initial=initial)
            else:
                ctx['actores'] = ActorPeliculaFormSet(instance=self.object)

        return ctx

    @transaction.atomic
    def form_valid(self, form):
        # 1) Guardar la película
        self.object = form.save()

        # 2) Reconstruir el formset con la instance YA creada y los datos del POST
        formset = ActorPeliculaFormSet(self.request.POST, instance=self.object)

        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            # si el formset falla, devolvés el template con errores
            return render(self.request, self.template_name, {
                'form': form,
                'actores': formset,
                'object': self.object,
            })


class PeliculasLista5(LoginRequiredMixin, SingleTableView):
    model = Pelicula
    table_class = PeliculaTable2
    template_name = "peliculaslistaoc5.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("idDirector", "idCategoria")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(nombre__icontains=q))
        return qs


class peliculaFormModificar3(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pelicula
    form_class = PeliculaForm2
    template_name = 'peliculaForm3.html'
    success_url = reverse_lazy('peliculaslistaoc5')
    permission_required = 'cinecarena.change_pelicula'
    raise_exception = False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "No tenés permiso para modificar películas.")
            return redirect('peliculaslistaoc5')
        # Si no está logueado, al login manteniendo el next
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def get_context_data(self, **kwargs):
        # ya no armamos formset de actores
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # --- Categoría nueva ---
        cat_pk = self.request.GET.get("categoria_nueva")
        if cat_pk and "idCategoria" in form.fields:
            form.initial["idCategoria"] = cat_pk
            form.fields["idCategoria"].initial = cat_pk
            try:
                form.instance.idCategoria_id = int(cat_pk)
            except (ValueError, TypeError):
                pass

        # --- Director nuevo ---
        dir_pk = self.request.GET.get("director_nuevo")
        if dir_pk and "idDirector" in form.fields:
            form.initial["idDirector"] = dir_pk
            form.fields["idDirector"].initial = dir_pk
            try:
                form.instance.idDirector_id = int(dir_pk)
            except (ValueError, TypeError):
                pass

        # --- Actor nuevo (solo preselección) ---
        act_pk = self.request.GET.get("actor_nuevo")
        if act_pk and "actores" in form.fields:
            try:
                actor = Actor.objects.get(pk=int(act_pk))
                # asegurar que aparezca en el queryset del widget
                form.fields["actores"].queryset = Actor.objects.all()
                # si estamos editando, sumamos a los ya seleccionados:
                inicial = list(form.initial.get("actores", [])) or \
                          list(form.instance.actores.values_list("pk", flat=True))
                if actor.pk not in inicial:
                    inicial.append(actor.pk)
                form.initial["actores"] = inicial
            except (Actor.DoesNotExist, ValueError, TypeError):
                pass

        return form

    @transaction.atomic
    def form_valid(self, form):
        # No hay formset de actores: Django guarda el M2M directo
        return super().form_valid(form)


class peliculaFormCrear3(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pelicula
    form_class = PeliculaForm2
    template_name = 'peliculaForm3.html'
    success_url = reverse_lazy('peliculaslistaoc5')
    permission_required = 'cinecarena.add_pelicula'

    def get_context_data(self, **kwargs):
        # ya no armamos formset de actores
        return super().get_context_data(**kwargs)

    # Preselecciones por querystring (igual que en Modificar)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # --- Categoría nueva ---
        cat_pk = self.request.GET.get("categoria_nueva")
        if cat_pk and "idCategoria" in form.fields:
            form.initial["idCategoria"] = cat_pk
            form.fields["idCategoria"].initial = cat_pk
            try:
                # en CreateView todavía no hay instance persistida; igual podés setearla
                form.instance.idCategoria_id = int(cat_pk)
            except (ValueError, TypeError):
                pass

        # --- Director nuevo ---
        dir_pk = self.request.GET.get("director_nuevo")
        if dir_pk and "idDirector" in form.fields:
            form.initial["idDirector"] = dir_pk
            form.fields["idDirector"].initial = dir_pk
            try:
                form.instance.idDirector_id = int(dir_pk)
            except (ValueError, TypeError):
                pass

        # --- Actor nuevo (preselección) ---
        act_pk = self.request.GET.get("actor_nuevo")
        if act_pk and "actores" in form.fields:
            try:
                actor_id = int(act_pk)
                # asegurar queryset (por si usás filtros dinámicos)
                form.fields["actores"].queryset = Actor.objects.all()
                # construir lista de ids
                inicial = list(form.initial.get("actores", []))
                if actor_id not in inicial:
                    inicial.append(actor_id)
                form.initial["actores"] = inicial
            except (ValueError, TypeError):
                pass

        return form

    @transaction.atomic
    def form_valid(self, form):
        # No hay formset de actores: Django guarda el M2M directo
        return super().form_valid(form)


class CategoriaCreateHX(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "_categoriaForm.html"

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        obj = form.save()
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "_categoriaSuccessOOB.html",
                {"obj": obj},
                status=200,
            )
        return super().form_valid(form)


class DirectorCreateHX(CreateView):
    model = Director
    form_class = DirectorForm
    template_name = "_directorForm.html"

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        obj = form.save()
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "_directorSuccessOOB.html",
                {"obj": obj},
                status=200,
            )
        return super().form_valid(form)


class ActorCreateHX(CreateView):
    model = Actor
    form_class = ActorForm
    template_name = "_actorForm.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["target_select"] = self.request.GET.get("target_select") or self.request.POST.get("target_select")
        return ctx

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        obj = form.save()
        if self.request.headers.get("HX-Request"):
            return render(self.request, "_actorSuccessOOB.html",
                          {"obj": obj,
                           "target_select": self.request.POST.get("target_select")}, status=200)
        return super().form_valid(form)


def Logout(request):
    logout(request)
    return redirect('/index')


def login_view(request):
    redirect_field_name = 'next'
    next_url = request.GET.get(redirect_field_name) or request.POST.get(redirect_field_name)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
            # opcional: conservar el username en el form
            return render(request, 'login.html', {'username': username, redirect_field_name: next_url})

    return render(request, 'login.html')