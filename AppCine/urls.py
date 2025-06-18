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
    ]