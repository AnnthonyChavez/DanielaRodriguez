# primer_parte/views.py

from django.shortcuts import render
from .models import PlatoTipico

def lista_platos(request):
    platos = PlatoTipico.objects.all().order_by('nombre') # Obtiene todos los platos de la base de datos
    context = {
        'platos': platos,
        'titulo': 'Listado de Platos Típicos de Ecuador'
    }
    return render(request, 'primer_parte/lista_platos.html', context) # Renderiza el template