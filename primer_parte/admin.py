# primer_parte/admin.py

from django.contrib import admin
from .models import PlatoTipico

@admin.register(PlatoTipico)
class PlatoTipicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region', 'ingredientes_principales') # Columnas a mostrar en la lista del admin
    search_fields = ('nombre', 'descripcion', 'region') # Campos por los que se puede buscar
    list_filter = ('region',) # Filtros laterales