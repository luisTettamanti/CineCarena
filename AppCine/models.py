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
    fechaNac = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    origen = models.CharField(max_length=50, blank=True, null=True, verbose_name="País de Origen")

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    nombre = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name='año')
    duracion = models.IntegerField(verbose_name='duración')
    idDirector = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name="director")
    imdb = models.IntegerField(blank=True, null=True, help_text="Puntaje en IMDB")
    idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="categoría")
    ordenNetflix = models.IntegerField(blank=True, null=True, help_text="Ranking en Netflix")
    caratula = models.URLField(blank=True, null=True, verbose_name="carátula")
    resenia = models.TextField(blank=True, null=True, verbose_name="reseña")
    actores = models.ManyToManyField(Actor, through='ActorPelicula', related_name='peliculas')

    def __str__(self):
        return self.nombre


class ActorPelicula(models.Model):
    idActor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    idPelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('idActor', 'idPelicula')  # evita el mismo actor repetido en la misma película