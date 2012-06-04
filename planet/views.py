""" Vistas definidas para app planet """
import feedparser
from planet.models import Blog
from django.shortcuts import render_to_response
import calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
