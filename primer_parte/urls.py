# primer_parte/urls.py

from django.urls import path
from . import views
# No necesitas 'include' aquí porque esta app no incluye otras apps
# Ni necesitas settings/static aquí, ya que el proyecto principal se encarga de eso

urlpatterns = [
    path('platos/', views.lista_platos, name='lista_platos'), # La URL específica para listar platos
]