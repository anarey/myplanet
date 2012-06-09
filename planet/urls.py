""" Fichero de configuracion de url de la app planet """

from django.conf.urls import patterns, url

urlpatterns = patterns('planet.views',
        url(r'^$','index'),
        url(r'^bloglist/$','blog_list'),
        url(r'^blogsearch/$','blog_search'),
        url(r'^blognew/$','blog_new'),
        #        url(r'^(?P<blog_id>\d+)/$', 'detail'),
)
