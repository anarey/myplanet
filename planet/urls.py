from django.conf.urls import patterns, include, url

urlpatterns = patterns('planet.views',
        url(r'^$','index'),
#        url(r'^(?P<blog_id>\d+)/$', 'detail'),
)
