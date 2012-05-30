# Create your views here.
import feedparser
from planet.models import Blog
#from django.http import HttpResponse
from django.shortcuts import render_to_response

#from time import mktime
#from datetime import datetime
import calendar

def index(request):
    blog_list = Blog.objects.all() ## Todos los blogs
    enable_list = []
    post_list = []
    for b in blog_list:
        if b.enable:  ##por cada feed activo
            i=0
#            enable_list.append(b.feed)
            enable_list.append(b)
            d = feedparser.parse(b.feed)
            for p in d['entries']:
                post = []
                date = calendar.timegm(p.published_parsed)
                post = [p.title, p.link, p.published_parsed,date, p.content[0].value]
                post_list.append(post)
            
#    return HttpResponse(enable_list)
    return render_to_response('planet/index.html',{'enable_list' : enable_list,'post_list':post_list})

#def detail(request,blog_id):
#    return HttpResponse("Details")
