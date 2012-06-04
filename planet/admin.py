""" Activar la configuración del modelo de datos blogs 
en la zona de administracion"""

from django.contrib import admin
from planet.models import Blog

admin.site.register(Blog)
