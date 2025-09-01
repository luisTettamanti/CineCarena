from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),

    path('pelicula/', views.pelicula, name='pelicula'),
    path('peliculadatos/', views.peliculadatos, name='peliculadatos'),
    path('peliculasLista/', views.peliculasLista, name='peliculaslista'),
    path('peliculaslistanetflix/', views.peliculaslistanetflix, name='peliculaslistanetflix'),
    path('peliculadatosnetflix/', views.peliculadatosnetflix, name='peliculadatosnetflix'),
    path('actoreslista/', views.actoreslista, name='actoreslista'),
    path('actordatos/<int:pk>/', views.actordatos, name='actordatos'),
    path('peliculaform/', views.peliculaForm, name='peliculaagregar'),
    path('peliculaform/<int:pk>/', views.peliculaForm, name='peliculamodificar'),
    path('peliculaborrar/<int:pk>/', views.peliculaBorrar, name='peliculaborrar'),
    path('peliculaconsultar/<int:pk>/', views.peliculaConsultar, name='peliculaconsultar'),

    path('peliculaslistaConForm/', views.peliculasListaConForm.as_view(), name='peliculasListaConForm'),
    path('peliculaAgregarConForm/', views.peliculaConFormAgregar.as_view(), name='peliculaAgregarConForm'),
    path('peliculaModificarConForm/<int:pk>/', views.peliculaConFormModificar.as_view(), name='peliculaModificarConForm'),
    path('peliculaBorrarConForm/<int:pk>/', views.peliculaConFormBorrar.as_view(), name='peliculaBorrarConForm'),
    path('peliculaDetalleConForm/<int:pk>/', views.peliculaConFormDetalle.as_view(), name='peliculaDetalleConForm'),

    path('peliculaCreate/', views.PeliculaCreateView.as_view(), name='peliculacreate'),
    path('peliculaUpdate/<int:pk>/', views.PeliculaUpdateView.as_view(),
         name='peliculaupdate'),
    path('peliculaDelete/<int:pk>/', views.PeliculaDeleteView.as_view(), name='peliculadelete'),
    path('peliculaDetail/<int:pk>/', views.PeliculaDetailView.as_view(), name='peliculadetail'),
    path('peliculaDetailoc/<int:pk>/', views.PeliculaDetailViewOC.as_view(), name='peliculadetailoc'),
    path('peliculasListaoc/', views.Peliculaslista.as_view(), name='peliculaslistaoc'),

    ]