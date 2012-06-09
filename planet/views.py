# -*- coding: utf-8 -*-
""" Vistas definidas para app planet """
import calendar
import feedparser

from django.template import RequestContext
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from planet.models import Blog
from planet.forms import BlogForm


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
    """ Vista que muestra el listado detallado de los distintos 
    blogs sindicados."""

    query_blog = Blog.objects.all()
    enable_blog = query_blog.filter(enable = True)
    return render_to_response('bloglist.html', {'enable_blog': enable_blog})    

def blog_search(request):
    """ vista que permite realizar una busqueda entre los feed que se muestran en el planet
    por autor o titulo del blogs"""
#    query = request.GET.get('word','')
    if 'word' in request.GET and request.GET['word']:
 #   if query:
        query = request.GET.get('word','')
        result_search = Blog.objects.filter( Q(name__icontains = query)| 
                Q(author__icontains = query), Q(enable = True))
        
        return render_to_response('blogsearch.html', {
            'result_search':result_search,
            'query' : query})
    else:
        return render_to_response('blogsearch.html', {'error':True})

def blog_new(request):
    if request.method == 'POST':
        blog_preform = BlogForm(request.POST)
        if blog_preform.is_valid():
            blog_form = blog_preform.cleaned_data
            ## Como todo fue bien, redireccion a otra pagina. por seguridad
            newlink = Blog()
            newlink.author = blog_form['author']
            newlink.name = blog_form['name']
            newlink.feed = blog_form['feed']
            newlink.enable = False
            newlink.save()
            return HttpResponseRedirect('/planet/bloglist/')
    else:
        ## Si no hay info en request.POST, 1 vez que entra: 
        ## formulario en blanco
        blog_preform = BlogForm()
    
    return render_to_response('blognew.html',{'blog_form': blog_preform}, 
            context_instance=RequestContext(request))
