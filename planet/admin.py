""" Configuracion del modelo en la zona de administracion """

from django.contrib import admin
from planet.models import Blog

admin.site.register(Blog)
