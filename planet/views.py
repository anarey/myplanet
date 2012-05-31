# Create your views here.
import feedparser
from planet.models import Blog
#from django.http import HttpResponse
from django.shortcuts import render_to_response

#from time import mktime
#from datetime import datetime
import calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
#            lista=[]
            for p in d['entries']:
               # post = []
                date = calendar.timegm(p.published_parsed)
               # post = [p.title, p.link, p.published_parsed,date, p.content[0].value]
               # post_list.append(post)
                post_list.append({'date':date,'title':p.title,'date_format':p.published,'content':p.content[0].value,'link':p.link,'author':b.author})
            list_aux = [(dict_["date"], dict_) for dict_ in post_list]
            list_aux.sort(reverse=True)
            order_post = [dist_ for (key,dist_) in list_aux]

            paginator = Paginator(order_post,6)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                posts = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                posts = paginator.page(paginator.num_pages)
#    return HttpResponse(enable_list)
    return render_to_response('index.html',{'enable_list' : enable_list,'post_list':posts})


##### Cambiando el nombre de las listas para mostrar los disccionarios.


#def detail(request,blog_id):
#    return HttpResponse("Details")
