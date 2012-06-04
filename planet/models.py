""" Definimos los modelos de la app """
from django.db import models

class Blog(models.Model):
    """ Objeto modelo """

    author = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    feed = models.URLField()
    enable = models.BooleanField()

    def __unicode__(self):
        return self.name

