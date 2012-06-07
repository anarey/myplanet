""" Vistas definidas para app planet """
import calendar
import feedparser

from django.db.models import Q
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from planet.models import Blog

def index(request):
    """ vista que muestra los post de todos los blogs ordenados por fecha
    de publicacion """

    ## Obtemos solo los objetos que cumplen dicha condicion
    ## Que estan activos
    query_blog = Blog.objects.all()
    enable_list = query_blog.filter(enable = True)
    post_list = []
    for blog_config in enable_list:
        post_config = feedparser.parse(blog_config.feed)
        for post in post_config['entries']:
            date = calendar.timegm(post.published_parsed)
            post_list.append({'date':date, 'title':post.title,
                'date_format':post.published, 'content':post.content[0].value,
                'link':post.link, 'author':blog_config.author})
    list_aux = [(dict_["date"], dict_) for dict_ in post_list]
    list_aux.sort(reverse=True)
    order_post = [dist_ for (key, dist_) in list_aux]

    paginator = Paginator(order_post, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
     # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
     # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render_to_response('index.html', {'enable_list' : enable_list,
        'post_list': posts, 'page_number': range(1, paginator.num_pages+1)})

def blog_list(request):
    """ Vista que muestra el listado detallado de los distintos blogs sindicados."""

    query_blog = Blog.objects.all()
    enable_blog = query_blog.filter(enable = True)
    return render_to_response('bloglist.html', {'enable_blog': enable_blog})    

def blog_search(request):
    """ vista que permite realizar una busqueda entre los feed que se muestran en el planet
    por autor o titulo del blogs"""
    query = request.GET.get('word','')
    if query:
        qs_search = (
                Q(name__icontains = query)| 
                Q(author__icontains = query)
                )
        result_search = Blog.objects.filter(qs_search)
    else:
        result_search = []
    return render_to_response('blogsearch.html', {
        'result_search':result_search,
        'query' : query})
