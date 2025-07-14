from django.db import models

# primer_parte/models.py

from django.db import models

# Borra la línea '# Create your models here.' y pega el siguiente código:
class PlatoTipico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Plato")
    descripcion = models.TextField(verbose_name="Descripción")
    region = models.CharField(max_length=50, blank=True, null=True, verbose_name="Región") # Ej: Costa, Sierra, Oriente, Galápagos
    ingredientes_principales = models.CharField(max_length=200, verbose_name="Ingredientes Principales")
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True, verbose_name="Imagen") # Opcional: para subir imágenes

    class Meta:
        verbose_name = "Plato Típico de Ecuador"
        verbose_name_plural = "Platos Típicos de Ecuador"
        ordering = ['nombre'] # Ordenar por nombre por defecto

    def __str__(self):
        return self.nombre
