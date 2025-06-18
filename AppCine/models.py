from django.db import models


class Director(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Actor(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    nombre = models.CharField(max_length=50)
    anio = models.IntegerField()
    duracion = models.IntegerField()
    idDirector = models.ForeignKey(Director, on_delete=models.CASCADE)
    imdb = models.IntegerField(blank=True, null=True)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ordenNetflix = models.IntegerField(blank=True, null=True)
    caratula = models.URLField(blank=True, null=True)
    resenia = models.TextField(blank=True, null=True)
    actores = models.ManyToManyField(Actor, through='ActorPelicula', related_name='peliculas')

    def __str__(self):
        return self.nombre


class ActorPelicula(models.Model):
    idActor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    idPelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)