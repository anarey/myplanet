# Create your views here.
from planet.models import Blog
from django.http import HttpResponse

def index(request):
    blog_list = Blog.objects.all() ## TODO solo los activos
#    enable_list = ', '.join([b.name for b in blog_list])
    enable_list = []
    for b in blog_list:
        if b.enable:
            enable_list.append(b.name)
    return HttpResponse(enable_list)

#def detail(request,blog_id):
#    return HttpResponse("Details")
