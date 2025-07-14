# platos_ecuador_project/urls.py

from django.contrib import admin
from django.urls import path, include # Asegúrate de que 'include' esté aquí
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración
    path('platos_ecuador/', include('primer_parte.urls')), # Incluye las URLs de tu aplicación 'primer_parte'
    # Puedes cambiar 'platos_ecuador/' a '' si quieres que sea la raíz del sitio
    # Si lo dejas como 'platos_ecuador/', la URL de tus platos será: http://127.0.0.1:8000/platos_ecuador/platos/
]

# Configuración para servir archivos de medios (imágenes) durante el desarrollo
# ¡IMPORTANTE! Esto solo funciona en modo DEBUG=True. No usar en producción.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)