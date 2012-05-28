from django.db import models

# Create your models here.
class Blog(models.Model):
    author = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    feed = models.URLField()
    enable = models.BooleanField()

    def __unicode__(self):
        return self.name

