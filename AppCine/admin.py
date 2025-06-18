from django.contrib import admin

from AppCine.models import Pelicula, Director, Actor, Categoria, ActorPelicula

admin.site.register(Pelicula)
admin.site.register(Director)
admin.site.register(Categoria)
admin.site.register(Actor)
admin.site.register(ActorPelicula)
