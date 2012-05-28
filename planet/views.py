# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Pagina del Planet")
#def detail(request,blog_id):
#    return HttpResponse("Details")
