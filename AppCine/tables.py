import django_tables2 as tables
from .models import Pelicula
from django.urls import reverse


class PeliculaTable(tables.Table):
    # Campo relacionado: ordena por el nombre del director
    director = tables.Column(
        accessor="idDirector.nombre",
        order_by=("idDirector__nombre",),
        verbose_name="Director",
        attrs={
            "th": {"class": "d-none d-md-table-cell"},
            "td": {"class": "d-none d-md-table-cell"},
        }
    )

    anio = tables.Column(
        attrs={
            "th": {"class": "d-none d-md-table-cell"},
            "td": {"class": "d-none d-md-table-cell"},
        }
    )

    nombre = tables.TemplateColumn(
        template_code="""
            <a class="text-decoration-none"
            style="cursor:pointer"
            data-bs-toggle="offcanvas"
            data-bs-target="#peliculaOffcanvas"
            hx-get="{% url 'peliculadetailoc' record.pk %}"
            hx-target="#offcanvasBody"
            hx-swap="innerHTML">
                {{ record.nombre }}
            </a>
        """,
        verbose_name="Nombre",
        order_by=("nombre",),
    )

    acciones = tables.TemplateColumn(
        template_code="""
            <a class="btn btn-primary me-2" href="{% url 'peliculamodificar2' record.pk %}">Modificar</a>
            <a class="btn btn-danger" href="{% url 'peliculaBorrarConForm' record.pk %}">Borrar</a>
            """,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {"class": "text-end text-nowrap"}
        },
    )

    class Meta:
        model = Pelicula
        # Solo muestra estas columnas (más 'director' y 'acciones' que definimos arriba)
        fields = ("id", "nombre", "anio")
        template_name = "django_tables2/bootstrap5.html"  # usa Bootstrap 5
        attrs = {
            "class": "table table-striped table-hover align-middle",
            "thead": {"class": "table-dark"},  # <thead>
            "th": {"class": "fw-semibold"},  # <th> de cabecera
            "tbody": {"class": "table-group-divider"},  # separador entre grupos (BS5)
        }
        sequence = ("id", "nombre", "director", "anio", "acciones")


class PeliculaTable2(tables.Table):
    # Campo relacionado: ordena por el nombre del director
    director = tables.Column(
        accessor="idDirector.nombre",
        order_by=("idDirector__nombre",),
        verbose_name="Director",
        attrs={
            "th": {"class": "d-none d-md-table-cell"},
            "td": {"class": "d-none d-md-table-cell"},
        }
    )

    anio = tables.Column(
        attrs={
            "th": {"class": "d-none d-md-table-cell"},
            "td": {"class": "d-none d-md-table-cell"},
        }
    )

    nombre = tables.TemplateColumn(
        template_code="""
            <a class="text-decoration-none"
            style="cursor:pointer"
            data-bs-toggle="offcanvas"
            data-bs-target="#peliculaOffcanvas"
            hx-get="{% url 'peliculadetailoc' record.pk %}"
            hx-target="#offcanvasBody"
            hx-swap="innerHTML">
                {{ record.nombre }}
            </a>
        """,
        verbose_name="Nombre",
        order_by=("nombre",),
    )

    acciones = tables.TemplateColumn(
        template_code="""
            <a class="btn btn-primary me-2" href="{% url 'peliculamodificar3' record.pk %}">Modificar</a>
            <a class="btn btn-danger" href="{% url 'peliculaBorrarConForm' record.pk %}">Borrar</a>
            """,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {"class": "text-end text-nowrap"}
        },
    )

    class Meta:
        model = Pelicula
        # Solo muestra estas columnas (más 'director' y 'acciones' que definimos arriba)
        fields = ("id", "nombre", "anio")
        template_name = "django_tables2/bootstrap5.html"  # usa Bootstrap 5
        attrs = {
            "class": "table table-striped table-hover align-middle",
            "thead": {"class": "table-dark"},  # <thead>
            "th": {"class": "fw-semibold"},  # <th> de cabecera
            "tbody": {"class": "table-group-divider"},  # separador entre grupos (BS5)
        }
        sequence = ("id", "nombre", "director", "anio", "acciones")


# { % if perms.cinecarena.change_pelicula %}
# { % endif %}