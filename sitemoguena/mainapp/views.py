from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render

def index( request: HttpRequest ):
    return render( request,
                   'mainapp/index.html',
                   {'title':'Главная страница.'}
           )







# ---------------------------------------------------------------------------------------------
# Срабатывает, если в любом представлении возн ош 404  , руками:    raise Http404()
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



